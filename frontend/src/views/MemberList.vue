<template>
  <div>
    <el-button type="primary" @click="showDialog()">新增会员</el-button>
    <el-input v-model="keyword" placeholder="搜索姓名/电话/卡号" style="width: 200px; margin-left: 10px" @keyup.enter="loadMembers" clearable />
    <el-button @click="loadMembers" style="margin-left: 5px">搜索</el-button>

    <el-table :data="members" stripe style="margin-top: 15px">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="phone" label="电话" width="130" />
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column prop="card_no" label="卡号" width="120" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">{{ row.status === 'active' ? '正常' : '停用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="join_date" label="加入日期" width="120" />
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

    <el-pagination
      v-model:current-page="page"
      :page-size="10"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="loadMembers"
      style="margin-top: 15px"
    />

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑会员' : '新增会员'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="姓名" required>
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="电话" required>
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="身份证">
          <el-input v-model="form.id_card" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status">
            <el-option label="正常" value="active" />
            <el-option label="停用" value="inactive" />
          </el-select>
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
import { getMembers, createMember, updateMember, deleteMember } from '../api/members'
import { ElMessage } from 'element-plus'

const members = ref([])
const keyword = ref('')
const page = ref(1)
const total = ref(0)
const dialogVisible = ref(false)
const form = ref({})

const loadMembers = async () => {
  const res = await getMembers({ keyword: keyword.value, page: page.value, size: 10 })
  members.value = Array.isArray(res) ? res : (res?.items || [])
  total.value = res?.total || members.value.length
}

const showDialog = (row) => {
  form.value = row ? { ...row } : { name: '', phone: '', email: '', id_card: '', address: '', status: 'active' }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (form.value.id) {
    await updateMember(form.value.id, form.value)
    ElMessage.success('更新成功')
  } else {
    await createMember(form.value)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadMembers()
}

const handleDelete = async (id) => {
  await deleteMember(id)
  ElMessage.success('删除成功')
  loadMembers()
}

onMounted(loadMembers)
</script>
