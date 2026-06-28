<template>
  <div class="teacher-question-detail">
    <div class="header">
      <el-button @click="goBack">← 返回题目管理</el-button>
      <h1>📝 题目详情（教师视图）</h1>
    </div>

    <div v-loading="loading" class="content">
      <!-- 题目信息（同学生端，但增加答案展示） -->
      <el-card class="question-info">
        <template #header>
          <div class="card-header">
            <span>{{ question.title || '未命名题目' }}</span>
            <el-tag :type="difficultyTagType(question.difficulty)">
              {{ difficultyText(question.difficulty) }}
            </el-tag>
          </div>
        </template>

        <div class="section">
          <h3>📖 题目描述</h3>
          <div class="description">{{ question.description }}</div>
        </div>

        <div v-if="question.create_table_sql" class="section">
          <h3>📊 建表语句</h3>
          <pre class="sql-block">{{ question.create_table_sql }}</pre>
        </div>

        <div class="sample-row">
          <div class="sample-item">
            <h3>📥 样例输入</h3>
            <pre class="sample">{{ question.sample_input || '无' }}</pre>
          </div>
          <div class="sample-item">
            <h3>📤 样例输出</h3>
            <pre class="sample">{{ question.sample_output || '无' }}</pre>
          </div>
        </div>

        <!-- ✅ 教师可见：正确答案 -->
        <div class="section answer-section">
          <h3>🔑 参考答案</h3>
          <div v-if="question.answers && question.answers.length > 0">
            <div v-for="(ans, idx) in question.answers" :key="idx" class="answer-item">
              <span class="answer-label">答案 {{ idx + 1 }}：</span>
              <pre class="answer-sql">{{ ans.correct_sql }}</pre>
            </div>
          </div>
          <div v-else class="no-answer">
            <span style="color: #909399;">暂未设置参考答案</span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getQuestionDetail } from '../../api/questions'

const route = useRoute()
const router = useRouter()
const questionId = computed(() => Number(route.params.id))

const loading = ref(false)
const question = ref<any>({})

const loadQuestion = async () => {
  loading.value = true
  try {
    const res = await getQuestionDetail(questionId.value)
    question.value = res.data || {}
  } catch (error) {
    ElMessage.error('加载题目失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/teacher/questions')
}

const difficultyTagType = (diff: string) => {
  switch (diff) {
    case 'easy': return 'success'
    case 'medium': return 'warning'
    case 'hard': return 'danger'
    default: return 'info'
  }
}

const difficultyText = (diff: string) => {
  switch (diff) {
    case 'easy': return '简单'
    case 'medium': return '中等'
    case 'hard': return '困难'
    default: return diff || '未知'
  }
}

onMounted(() => {
  loadQuestion()
})
</script>

<style scoped>
/* 复用学生端样式，略... */
</style>