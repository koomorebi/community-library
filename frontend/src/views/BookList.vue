<template>
  <div>
    <el-button type="primary" @click="showDialog()">新增图书</el-button>
    <el-input v-model="keyword" placeholder="搜索书名/作者" style="width: 200px; margin-left: 10px" @keyup.enter="loadBooks" clearable />
    <el-button @click="loadBooks" style="margin-left: 5px">搜索</el-button>

    <el-table :data="books" stripe style="margin-top: 15px">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="书名" />
      <el-table-column prop="author" label="作者" />
      <el-table-column prop="isbn" label="ISBN" width="140" />
      <el-table-column label="分类" width="80">
        <template #default="{ row }">
          {{ row.category?.name || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="total_copies" label="总库存" width="80" />
      <el-table-column prop="available_copies" label="可借" width="80" />
      <el-table-column label="操作" width="280">
        <template #default="{ row }">
          <el-button size="small" @click="showDialog(row)">编辑</el-button>
          <el-button size="small" type="success" @click="showHistory(row)">借阅历史</el-button>
          <el-popconfirm title="确定删除？" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="page"
      :page-size="10"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="loadBooks"
      style="margin-top: 15px"
    />

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑图书' : '新增图书'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="书名" required>
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="作者" required>
          <el-input v-model="form.author" />
        </el-form-item>
        <el-form-item label="ISBN">
          <el-input v-model="form.isbn" />
        </el-form-item>
        <el-form-item label="出版社">
          <el-input v-model="form.publisher" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category_id" placeholder="选择分类">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="库存数量">
          <el-input-number v-model="form.total_copies" :min="1" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 借阅历史对话框 -->
    <el-dialog v-model="historyVisible" :title="`${historyBook.title} - 借阅历史`" width="700px">
      <div style="margin-bottom: 10px; color: #909399">
        共 {{ historyData.total_borrows || 0 }} 次借阅
      </div>
      <el-table :data="historyData.history" stripe>
        <el-table-column prop="member_name" label="借阅人" width="100" />
        <el-table-column prop="member_card_no" label="卡号" width="130" />
        <el-table-column label="借阅日期" width="160">
          <template #default="{ row }">
            {{ formatDate(row.borrow_date) }}
          </template>
        </el-table-column>
        <el-table-column label="应还日期" width="120">
          <template #default="{ row }">
            {{ row.due_date }}
          </template>
        </el-table-column>
        <el-table-column label="实还日期" width="160">
          <template #default="{ row }">
            {{ row.return_date ? formatDate(row.return_date) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="renew_count" label="续借次数" width="80" align="center" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'borrowed' ? 'warning' : 'success'">
              {{ row.status === 'borrowed' ? '借阅中' : '已归还' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!historyData.history?.length" style="text-align: center; padding: 20px; color: #909399">
        暂无借阅记录
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBooks, createBook, updateBook, deleteBook } from '../api/books'
import { getCategories } from '../api/categories'
import { getBookHistory } from '../api/books'
import { ElMessage } from 'element-plus'

const books = ref([])
const categories = ref([])
const keyword = ref('')
const page = ref(1)
const total = ref(0)
const dialogVisible = ref(false)
const form = ref({})

// 借阅历史相关
const historyVisible = ref(false)
const historyBook = ref({})
const historyData = ref({ total_borrows: 0, history: [] })

const loadBooks = async () => {
  const res = await getBooks({ keyword: keyword.value, page: page.value, size: 10 })
  books.value = Array.isArray(res) ? res : (res?.items || [])
  total.value = res?.total || books.value.length
}

const loadCategories = async () => {
  const res = await getCategories()
  categories.value = Array.isArray(res) ? res : []
}

const showDialog = (row) => {
  form.value = row ? { ...row } : { title: '', author: '', isbn: '', publisher: '', category_id: null, total_copies: 1, description: '' }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (form.value.id) {
    await updateBook(form.value.id, form.value)
    ElMessage.success('更新成功')
  } else {
    await createBook(form.value)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadBooks()
}

const handleDelete = async (id) => {
  await deleteBook(id)
  ElMessage.success('删除成功')
  loadBooks()
}

// 显示借阅历史
const showHistory = async (row) => {
  historyBook.value = row
  historyVisible.value = true
  try {
    const res = await getBookHistory(row.id)
    historyData.value = res || { total_borrows: 0, history: [] }
  } catch (error) {
    console.error('获取借阅历史失败:', error)
    ElMessage.error('获取借阅历史失败')
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadBooks()
  loadCategories()
})
</script>
