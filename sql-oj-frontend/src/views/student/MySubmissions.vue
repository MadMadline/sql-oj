<template>
  <div class="submissions-container">
    <div class="header">
      <el-button @click="goBack">← 返回</el-button>
      <h1>我的提交记录</h1>
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

    <div class="pagination">
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

const router = useRouter()

const submissions = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const truncateSQL = (sql: string) => {
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

const loadSubmissions = async () => {
  loading.value = true
  try {
    const res = await getSubmissions({ page: currentPage.value })
    submissions.value = res.data.results
    total.value = res.data.count
  } catch (error) {
    ElMessage.error('加载提交记录失败')
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