<template>
  <div>
    <el-button type="primary" @click="showDialog()">新增分类</el-button>
    <el-table :data="categories" stripe style="margin-top: 15px">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="showDialog(row)">编辑</el-button>
          <el-popconfirm title="确定删除？" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑分类' : '新增分类'" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories, createCategory, updateCategory, deleteCategory } from '../api/categories'
import { ElMessage } from 'element-plus'

const categories = ref([])
const dialogVisible = ref(false)
const form = ref({})

const loadCategories = async () => {
  const res = await getCategories()
  categories.value = Array.isArray(res) ? res : []
}

const showDialog = (row) => {
  form.value = row ? { ...row } : { name: '', sort_order: 0 }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (form.value.id) {
    await updateCategory(form.value.id, form.value)
    ElMessage.success('更新成功')
  } else {
    await createCategory(form.value)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadCategories()
}

const handleDelete = async (id) => {
  await deleteCategory(id)
  ElMessage.success('删除成功')
  loadCategories()
}

onMounted(loadCategories)
</script>
