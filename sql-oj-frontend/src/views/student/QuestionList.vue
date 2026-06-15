<template>
  <div class="question-list-container">
    <div class="header">
      <h1>SQL 题库</h1>
      <div class="user-info">
        <span>欢迎，{{ userStore.user?.username }}</span>
        <el-button type="primary" link @click="goToSubmissions">我的提交</el-button>
        <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
      </div>
    </div>

    <el-table :data="questions" v-loading="loading" stripe>
      <el-table-column prop="id" label="题号" width="80" />
      <el-table-column prop="description" label="题目描述" min-width="300">
        <template #default="{ row }">
          <div class="description-preview">{{ truncateDescription(row.description) }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="difficulty" label="难度" width="100">
        <template #default="{ row }">
          <el-tag :type="difficultyTagType(row.difficulty)">
            {{ difficultyText(row.difficulty) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="goToDetail(row.id)">
            开始答题
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        @current-change="loadQuestions"
        layout="prev, pager, next"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../../stores/user'

const router = useRouter()
const userStore = useUserStore()

// ========== Mock 数据（后端好了后删除，改用真实 API）==========
const mockQuestions = [
  { id: 1, description: '查询所有学生的姓名和年龄', difficulty: 'easy' },
  { id: 2, description: '查询成绩大于80分的学生姓名', difficulty: 'easy' },
  { id: 3, description: '查询每个班级的学生数量', difficulty: 'medium' },
  { id: 4, description: '查询平均成绩最高的前3名学生', difficulty: 'hard' },
]
// ============================================================

const questions = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const truncateDescription = (desc: string) => {
  if (desc.length > 100) return desc.substring(0, 100) + '...'
  return desc
}

const difficultyTagType = (difficulty: string) => {
  switch (difficulty) {
    case 'easy': return 'success'
    case 'medium': return 'warning'
    case 'hard': return 'danger'
    default: return 'info'
  }
}

const difficultyText = (difficulty: string) => {
  switch (difficulty) {
    case 'easy': return '简单'
    case 'medium': return '中等'
    case 'hard': return '困难'
    default: return difficulty
  }
}

const loadQuestions = async () => {
  loading.value = true
  try {
    // TODO: 后端好了后，替换成真实 API 调用
    // const res = await getQuestions({ page: currentPage.value })
    // questions.value = res.data.results
    // total.value = res.data.count
    
    // 临时 Mock
    setTimeout(() => {
      questions.value = mockQuestions
      total.value = mockQuestions.length
      loading.value = false
    }, 500)
  } catch (error) {
    ElMessage.error('加载题目列表失败')
    loading.value = false
  }
}

const goToDetail = (id: number) => {
  router.push(`/questions/${id}`)
}

const goToSubmissions = () => {
  router.push('/submissions')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  })
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.question-list-container {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f7fa;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}
.description-preview {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>