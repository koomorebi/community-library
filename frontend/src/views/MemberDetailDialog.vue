<template>
  <el-dialog
    v-model="visible"
    :title="memberInfo ? `${memberInfo.name} - 会员详情` : '会员详情'"
    width="800px"
    @close="handleClose"
  >
    <div v-if="loading" style="text-align: center; padding: 40px;">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <div v-else-if="memberInfo">
      <!-- 个人信息 -->
      <el-descriptions title="个人信息" :column="2" border>
        <el-descriptions-item label="姓名">{{ memberInfo.name }}</el-descriptions-item>
        <el-descriptions-item label="卡号">{{ memberInfo.card_no }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ memberInfo.phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ memberInfo.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="身份证">{{ memberInfo.id_card || '-' }}</el-descriptions-item>
        <el-descriptions-item label="地址" :span="2">{{ memberInfo.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="最大借阅数">{{ memberInfo.max_borrows }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="memberInfo.status === 'active' ? 'success' : 'danger'">
            {{ memberInfo.status === 'active' ? '正常' : '冻结' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ memberInfo.created_at }}</el-descriptions-item>
      </el-descriptions>

      <!-- 统计卡片 -->
      <el-row :gutter="20" style="margin: 20px 0;">
        <el-col :span="8">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-value">{{ stats.total_borrows }}</div>
            <div class="stat-label">总借阅次数</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-value">{{ stats.current_borrows }}</div>
            <div class="stat-label">当前借阅</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="stat-card stat-danger">
            <div class="stat-value">{{ stats.overdue_count }}</div>
            <div class="stat-label">逾期次数</div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 借阅历史 -->
      <h4>借阅历史（最近20条）</h4>
      <el-table :data="borrowHistory" border max-height="300">
        <el-table-column prop="book_title" label="书名" />
        <el-table-column prop="book_author" label="作者" width="100" />
        <el-table-column prop="borrow_date" label="借阅日期" width="160" />
        <el-table-column prop="due_date" label="应还日期" width="120" />
        <el-table-column prop="return_date" label="实还日期" width="160" />
        <el-table-column prop="renew_count" label="续借" width="60" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">
              {{ statusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <template #footer>
      <el-button @click="visible = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import { getMemberDetail } from '../api/members'

const props = defineProps({
  modelValue: Boolean,
  memberId: Number,
})

const emit = defineEmits(['update:modelValue'])

const visible = ref(false)
const loading = ref(false)
const memberInfo = ref(null)
const stats = ref({ total_borrows: 0, current_borrows: 0, overdue_count: 0 })
const borrowHistory = ref([])

const statusType = (s) => ({ borrowed: 'primary', returned: 'success', overdue: 'danger' }[s] || 'info')
const statusText = (s) => ({ borrowed: '借阅中', returned: '已归还', overdue: '逾期' }[s] || s)

watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val && props.memberId) {
    loadDetail()
  }
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

async function loadDetail() {
  loading.value = true
  try {
    const res = await getMemberDetail(props.memberId)
    memberInfo.value = res.member
    stats.value = res.stats
    borrowHistory.value = res.borrow_history
  } catch (e) {
    console.error('加载会员详情失败', e)
  } finally {
    loading.value = false
  }
}

function handleClose() {
  memberInfo.value = null
  stats.value = { total_borrows: 0, current_borrows: 0, overdue_count: 0 }
  borrowHistory.value = []
}
</script>

<style scoped>
.stat-card {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}

.stat-danger .stat-value {
  color: #f56c6c;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}
</style>
