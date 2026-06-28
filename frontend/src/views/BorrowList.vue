<template>
  <div>
    <h3>借阅管理</h3>
    <el-button type="primary" @click="showBorrowDialog">借书</el-button>
    <el-button @click="load">刷新</el-button>

    <!-- 筛选按钮 -->
    <div style="margin: 15px 0;">
      <el-radio-group v-model="statusFilter" @change="load">
        <el-radio-button label="all">全部</el-radio-button>
        <el-radio-button label="borrowed">借阅中</el-radio-button>
        <el-radio-button label="returned">已归还</el-radio-button>
        <el-radio-button label="overdue">逾期</el-radio-button>
      </el-radio-group>
    </div>

    <el-table :data="items" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="书名">
        <template #default="{ row }">
          {{ row.book?.title }}
        </template>
      </el-table-column>
      <el-table-column label="借阅人">
        <template #default="{ row }">
          <el-link type="primary" @click="showMemberDetail(row.member?.id)">
            {{ row.member?.name }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column prop="borrow_date" label="借阅日期" width="160" />
      <el-table-column prop="due_date" label="应还日期" width="120" />
      <el-table-column prop="return_date" label="实还日期" width="160" />
      <el-table-column prop="renew_count" label="续借次数" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ statusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="doReturn(row)" v-if="row.status === 'borrowed' || row.status === 'overdue'">归还</el-button>
          <el-button size="small" @click="doRenew(row)" v-if="row.status === 'borrowed'">续借</el-button>
          <el-button size="small" type="danger" @click="doUndo(row)" v-if="row.status === 'borrowed'">撤销</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="page"
      :page-size="20"
      :total="total"
      @current-change="load"
      layout="prev, pager, next"
      style="margin-top: 10px"
    />

    <!-- 借书对话框 -->
    <el-dialog v-model="dialogVisible" title="借书">
      <el-form :model="form" label-width="80px">
        <el-form-item label="会员ID">
          <el-input v-model.number="form.member_id" />
        </el-form-item>
        <el-form-item label="图书ID">
          <el-input v-model.number="form.book_id" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="doBorrow">确定</el-button>
      </template>
    </el-dialog>

    <!-- 用户详情弹窗 -->
    <MemberDetailDialog v-model="memberDetailVisible" :member-id="currentMemberId" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getBorrows, borrowBook, returnBook, renewBook, undoBorrow } from '../api/borrows'
import MemberDetailDialog from './MemberDetailDialog.vue'

const items = ref([])
const total = ref(0)
const page = ref(1)
const statusFilter = ref('all')
const dialogVisible = ref(false)
const memberDetailVisible = ref(false)
const currentMemberId = ref(null)
const form = ref({ member_id: '', book_id: '' })

const statusType = (s) => ({ borrowed: 'primary', returned: 'success', overdue: 'danger' }[s] || 'info')
const statusText = (s) => ({ borrowed: '借阅中', returned: '已归还', overdue: '逾期' }[s] || s)

async function load() {
  const params = { page: page.value, page_size: 20 }
  if (statusFilter.value !== 'all') {
    params.status = statusFilter.value
  }
  const res = await getBorrows(params)
  items.value = res.items
  total.value = res.total
}

function showBorrowDialog() {
  form.value = { member_id: '', book_id: '' }
  dialogVisible.value = true
}

async function doBorrow() {
  await borrowBook(form.value)
  dialogVisible.value = false
  ElMessage.success('借书成功')
  load()
}

async function doReturn(row) {
  await ElMessageBox.confirm('确认归还？')
  await returnBook({ borrow_id: row.id })
  ElMessage.success('归还成功')
  load()
}

async function doRenew(row) {
  await ElMessageBox.confirm('确认续借？')
  await renewBook({ borrow_id: row.id })
  ElMessage.success('续借成功')
  load()
}

async function doUndo(row) {
  await ElMessageBox.confirm('确认撤销此借阅？')
  await undoBorrow(row.id)
  ElMessage.success('撤销成功')
  load()
}

function showMemberDetail(memberId) {
  if (memberId) {
    currentMemberId.value = memberId
    memberDetailVisible.value = true
  }
}

onMounted(load)
</script>
