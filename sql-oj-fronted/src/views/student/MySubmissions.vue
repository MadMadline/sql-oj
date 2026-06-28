<template>
  <div class="submissions-container">
    <div class="header">
      <el-button @click="goBack">← 返回</el-button>
      <h1>📝 我的提交记录</h1>
    </div>

    <el-table :data="submissions" v-loading="loading" stripe>
      <el-table-column prop="id" label="提交ID" width="80" />
      <el-table-column prop="question" label="题目ID" width="80" />
      <el-table-column prop="submitted_sql" label="提交的SQL" min-width="250">
        <template #default="{ row }">
          <div class="sql-preview">{{ truncateSQL(row.submitted_sql) }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="execution_status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.execution_status)">
            {{ row.execution_status || 'PENDING' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="score" label="得分" width="80" />
      <el-table-column prop="created_at" label="提交时间" width="180" />
    </el-table>

    <!-- 分页（如果后端支持分页才显示） -->
    <div v-if="total > 0" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        @current-change="loadSubmissions"
        layout="prev, pager, next"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getSubmissions } from '../../api/submissions'

const router = useRouter()

const submissions = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const truncateSQL = (sql: string) => {
  if (!sql) return ''
  if (sql.length > 80) return sql.substring(0, 80) + '...'
  return sql
}

const statusTagType = (status: string) => {
  switch (status) {
    case 'ACCEPTED': return 'success'
    case 'WRONG_ANSWER': return 'danger'
    case 'TIMEOUT': return 'warning'
    default: return 'info'
  }
}

// ✅ 加载提交记录（兼容不同后端返回格式）
const loadSubmissions = async () => {
  loading.value = true
  try {
    // 先尝试不带参数请求，避免参数不匹配
    const res = await getSubmissions()
    
    // 兼容不同的返回格式
    const data = res.data || {}
    submissions.value = data.results || data || []
    total.value = data.count || submissions.value.length || 0
    
    console.log('✅ 提交记录加载成功，共', submissions.value.length, '条')
  } catch (error: any) {
    console.error('❌ 加载提交记录失败:', error.response?.data || error.message)
    ElMessage.error('加载提交记录失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/questions')
}

onMounted(() => {
  loadSubmissions()
})
</script>

<style scoped>
.submissions-container {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f7fa;
}
.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  background: white;
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.sql-preview {
  font-family: monospace;
  font-size: 12px;
  color: #606266;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>