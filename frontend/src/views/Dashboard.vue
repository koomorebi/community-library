<template>
  <div>
    <!-- 统计卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>总藏书</template>
          <div class="stat-num">{{ stats.total_books || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>借出中</template>
          <div class="stat-num" style="color: #e6a23c">{{ stats.borrowed_count || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>逾期未还</template>
          <div class="stat-num" style="color: #f56c6c">{{ stats.overdue_count || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>今日借还</template>
          <div class="stat-num" style="color: #67c23a">{{ stats.today_borrows || 0 }} / {{ stats.today_returns || 0 }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 热度排行榜 -->
    <el-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>📚 借阅热度排行榜</span>
          <div>
            <el-radio-group v-model="rankPeriod" size="small" @change="loadRanking">
              <el-radio-button label="monthly">月榜</el-radio-button>
              <el-radio-button label="yearly">年榜</el-radio-button>
              <el-radio-button label="all">总榜</el-radio-button>
            </el-radio-group>
          </div>
        </div>
      </template>
      
      <!-- 月/年选择器 -->
      <div v-if="rankPeriod !== 'all'" style="margin-bottom: 15px">
        <el-date-picker
          v-if="rankPeriod === 'monthly'"
          v-model="selectedDate"
          type="month"
          placeholder="选择月份"
          size="small"
          @change="loadRanking"
        />
        <el-date-picker
          v-if="rankPeriod === 'yearly'"
          v-model="selectedDate"
          type="year"
          placeholder="选择年份"
          size="small"
          @change="loadRanking"
        />
        <span style="margin-left: 10px; color: #909399">{{ rankingData.period_label }}</span>
      </div>

      <!-- 排行榜表格 -->
      <el-table :data="rankingData.ranking" stripe style="width: 100%">
        <el-table-column label="排名" width="80" align="center">
          <template #default="scope">
            <div class="rank-badge" :class="getRankClass(scope.row.rank)">
              {{ scope.row.rank }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="书名" />
        <el-table-column prop="author" label="作者" width="120" />
        <el-table-column label="借阅次数" width="100" align="center">
          <template #default="scope">
            <el-tag type="warning">{{ scope.row.borrow_count }} 次</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="!rankingData.ranking?.length" style="text-align: center; padding: 20px; color: #909399">
        暂无借阅数据
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStats } from '../api/stats'
import { getRanking } from '../api/stats'

const stats = ref({})
const rankPeriod = ref('all')
const selectedDate = ref(new Date())
const rankingData = ref({ period_label: '全部时间', ranking: [] })

// 加载排行榜
const loadRanking = async () => {
  try {
    const params = { period: rankPeriod.value }
    
    if (rankPeriod.value === 'monthly' && selectedDate.value) {
      const date = new Date(selectedDate.value)
      params.year = date.getFullYear()
      params.month = date.getMonth() + 1
    } else if (rankPeriod.value === 'yearly' && selectedDate.value) {
      params.year = new Date(selectedDate.value).getFullYear()
    }
    
    const res = await getRanking(params)
    rankingData.value = res || { period_label: '全部时间', ranking: [] }
  } catch (error) {
    console.error('加载排行榜失败:', error)
  }
}

// 排名样式
const getRankClass = (rank) => {
  if (rank === 1) return 'rank-gold'
  if (rank === 2) return 'rank-silver'
  if (rank === 3) return 'rank-bronze'
  return ''
}

onMounted(async () => {
  try {
    const res = await getStats()
    stats.value = res || {}
  } catch {}
  
  await loadRanking()
})
</script>

<style scoped>
.stat-num {
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  padding: 20px 0;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-weight: bold;
  background: #f0f0f0;
}

.rank-gold {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: white;
}

.rank-silver {
  background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
  color: white;
}

.rank-bronze {
  background: linear-gradient(135deg, #CD7F32, #A0522D);
  color: white;
}
</style>
