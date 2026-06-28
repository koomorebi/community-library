<template>
  <div>
    <h3>提醒设置</h3>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>到期提醒配置</span>
          <el-button type="primary" size="small" @click="saveConfig">保存配置</el-button>
        </div>
      </template>

      <el-form :model="config" label-width="120px">
        <!-- 提醒方式 -->
        <el-form-item label="提醒方式">
          <el-checkbox-group v-model="config.methods">
            <el-checkbox label="email">邮件提醒</el-checkbox>
            <el-checkbox label="sms">短信提醒</el-checkbox>
            <el-checkbox label="system">站内通知</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <!-- 提醒时间 -->
        <el-form-item label="提醒时间">
          <el-checkbox-group v-model="config.remind_days">
            <el-checkbox :label="7">到期前7天</el-checkbox>
            <el-checkbox :label="3">到期前3天</el-checkbox>
            <el-checkbox :label="1">到期前1天</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <!-- 邮件配置 -->
        <el-divider content-position="left">邮件配置</el-divider>

        <el-form-item label="SMTP服务器">
          <el-input v-model="config.email.smtp_host" placeholder="smtp.qq.com" />
        </el-form-item>

        <el-form-item label="SMTP端口">
          <el-input v-model.number="config.email.smtp_port" placeholder="465" />
        </el-form-item>

        <el-form-item label="发件邮箱">
          <el-input v-model="config.email.from_email" placeholder="your@email.com" />
        </el-form-item>

        <el-form-item label="授权码">
          <el-input v-model="config.email.auth_code" type="password" placeholder="邮箱授权码" show-password />
        </el-form-item>

        <el-form-item label="发件人名称">
          <el-input v-model="config.email.from_name" placeholder="社区图书馆" />
        </el-form-item>

        <!-- 短信配置 -->
        <el-divider content-position="left">短信配置</el-divider>

        <el-form-item label="服务商">
          <el-select v-model="config.sms.provider" placeholder="选择短信服务商">
            <el-option label="阿里云短信" value="aliyun" />
            <el-option label="腾讯云短信" value="tencent" />
          </el-select>
        </el-form-item>

        <el-form-item label="AccessKey">
          <el-input v-model="config.sms.access_key" placeholder="AccessKey ID" />
        </el-form-item>

        <el-form-item label="SecretKey">
          <el-input v-model="config.sms.secret_key" type="password" placeholder="AccessKey Secret" show-password />
        </el-form-item>

        <el-form-item label="短信签名">
          <el-input v-model="config.sms.sign_name" placeholder="短信签名" />
        </el-form-item>

        <el-form-item label="模板ID">
          <el-input v-model="config.sms.template_id" placeholder="短信模板ID" />
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 测试区域 -->
    <el-card style="margin-top: 20px;">
      <template #header>
        <span>测试发送</span>
      </template>

      <el-form :inline="true">
        <el-form-item label="测试手机号">
          <el-input v-model="testPhone" placeholder="输入手机号" />
        </el-form-item>
        <el-form-item label="测试邮箱">
          <el-input v-model="testEmail" placeholder="输入邮箱" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="sendTest">发送测试</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 提醒日志 -->
    <el-card style="margin-top: 20px;">
      <template #header>
        <span>最近提醒记录</span>
      </template>

      <el-table :data="remindLogs" border>
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="member" label="会员" width="100" />
        <el-table-column prop="book" label="图书" />
        <el-table-column prop="method" label="方式" width="80" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === '成功' ? 'success' : 'danger'" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const config = ref({
  methods: ['system'],
  remind_days: [3],
  email: {
    smtp_host: 'smtp.qq.com',
    smtp_port: 465,
    from_email: '',
    auth_code: '',
    from_name: '社区图书馆',
  },
  sms: {
    provider: 'aliyun',
    access_key: '',
    secret_key: '',
    sign_name: '',
    template_id: '',
  },
})

const testPhone = ref('')
const testEmail = ref('')

// 模拟提醒日志
const remindLogs = ref([
  { time: '2026-06-27 10:00:00', member: '会员A', book: '测试图书A', method: '站内', status: '成功' },
  { time: '2026-06-26 15:30:00', member: '会员B', book: '测试图书B', method: '邮件', status: '成功' },
])

function saveConfig() {
  // 保存到 localStorage
  localStorage.setItem('remind_config', JSON.stringify(config.value))
  ElMessage.success('配置已保存')
}

function sendTest() {
  if (!testPhone.value && !testEmail.value) {
    ElMessage.warning('请输入测试手机号或邮箱')
    return
  }
  ElMessage.success('测试消息已发送（模拟）')
}

// 加载配置
const saved = localStorage.getItem('remind_config')
if (saved) {
  config.value = JSON.parse(saved)
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
