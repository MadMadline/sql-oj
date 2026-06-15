<template>
  <div class="manage-container">
    <div class="header">
      <h1>📝 题目管理</h1>
      <div class="actions">
        <el-button type="primary" @click="goToCreate">+ 创建题目</el-button>
        <el-button type="danger" @click="handleLogout">退出</el-button>
      </div>
    </div>

    <el-table :data="questions" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="description" label="题目描述" min-width="250" />
      <el-table-column prop="difficulty" label="难度" width="100">
        <template #default="{ row }">
          <el-tag :type="difficultyTag(row.difficulty)">
            {{ difficultyText(row.difficulty) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="goToEdit(row.id)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../../stores/user'
import { getQuestions } from '../../api/questions'

const router = useRouter()
const userStore = useUserStore()

const questions = ref<any[]>([])
const loading = ref(false)

const difficultyTag = (diff: string) => {
  if (diff === 'easy') return 'success'
  if (diff === 'medium') return 'warning'
  return 'danger'
}

const difficultyText = (diff: string) => {
  if (diff === 'easy') return '简单'
  if (diff === 'medium') return '中等'
  return '困难'
}

const loadQuestions = async () => {
  loading.value = true
  try {
    const res = await getQuestions()
    questions.value = res.data.results || res.data
  } catch (error) {
    ElMessage.error('加载题目失败')
  } finally {
    loading.value = false
  }
}

const goToCreate = () => {
  router.push('/teacher/questions/create')
}

const goToEdit = (id: number) => {
  router.push(`/teacher/questions/create?id=${id}`)
}

const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除这道题吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    // TODO: 调用删除 API
    ElMessage.success('删除成功')
    loadQuestions()
  })
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
  ElMessage.success('已退出')
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.manage-container {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f7fa;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.actions {
  display: flex;
  gap: 12px;
}
</style>