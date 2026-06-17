<template>
  <div class="question-detail-container">
    <div class="header">
      <el-button @click="goBack">← 返回题目列表</el-button>
      <h1>📝 题目详情</h1>
    </div>

    <div v-loading="loading" class="content">
      <!-- 题目信息 -->
      <el-card class="question-info">
        <template #header>
          <div class="card-header">
            <span class="question-title">{{ question.title || '未命名题目' }}</span>
            <el-tag :type="difficultyTagType(question.difficulty)">
              {{ difficultyText(question.difficulty) }}
            </el-tag>
          </div>
        </template>

        <!-- 题目描述（完整题干） -->
        <div class="section">
          <h3>📖 题目描述</h3>
          <div class="description">{{ question.description }}</div>
        </div>

        <!-- ✅ 建表语句（美化展示） -->
        <div v-if="question.create_table_sql" class="section">
          <h3>📊 建表语句</h3>
          <div class="sql-block-wrapper">
            <div class="sql-toolbar">
              <span class="sql-lang">SQL</span>
              <el-button size="small" text @click="copySql(question.create_table_sql)">
                📋 复制
              </el-button>
            </div>
            <pre class="sql-block"><code>{{ question.create_table_sql }}</code></pre>
          </div>
        </div>

        <!-- 样例输入/输出 -->
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

        <!-- ❌ 学生端不显示答案（正确答案仅供教师查看） -->
      </el-card>

      <!-- SQL 编辑器 -->
      <el-card class="sql-editor">
        <template #header>
          <span>✏️ 编写你的 SQL</span>
        </template>
        <el-input
          v-model="sqlCode"
          type="textarea"
          :rows="10"
          placeholder="请输入你的 SQL 语句..."
          class="sql-textarea"
        />
        <div class="actions">
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            🚀 提交判题
          </el-button>
          <el-button @click="resetCode">重置</el-button>
        </div>
      </el-card>

      <!-- 判题结果 -->
      <el-card v-if="result" class="result">
        <template #header>
          <span>📊 判题结果</span>
        </template>
        <div class="result-content">
          <div class="status">
            <span>状态：</span>
            <el-tag :type="statusTagType(result.execution_status)">
              {{ result.execution_status || 'PENDING' }}
            </el-tag>
          </div>
          <div class="score">
            <span>得分：</span>
            <span class="score-value">{{ result.score ?? 0 }}</span>
          </div>
          <div v-if="result.details" class="details">
            <h4>详细结果</h4>
            <pre>{{ JSON.stringify(result.details, null, 2) }}</pre>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getQuestionDetail } from '../../api/questions'
import { submitSQL } from '../../api/submissions'

const route = useRoute()
const router = useRouter()
const questionId = computed(() => Number(route.params.id))

const loading = ref(false)
const submitting = ref(false)
const question = ref<any>({})
const sqlCode = ref('')
const result = ref<any>(null)

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

const handleSubmit = async () => {
  if (!sqlCode.value.trim()) {
    ElMessage.warning('请输入 SQL 语句')
    return
  }

  submitting.value = true
  try {
    const res = await submitSQL({
      question_id: questionId.value,
      submitted_sql: sqlCode.value,
      exam_id: null
    })
    result.value = res.data
    ElMessage.success('提交成功 ✅')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.error || '提交失败')
  } finally {
    submitting.value = false
  }
}

const resetCode = () => {
  sqlCode.value = ''
  result.value = null
}

const goBack = () => {
  router.push('/questions')
}

const copySql = (sql: string) => {
  navigator.clipboard?.writeText(sql).then(() => {
    ElMessage.success('已复制到剪贴板')
  }).catch(() => {
    // 降级方案
    const textarea = document.createElement('textarea')
    textarea.value = sql
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    ElMessage.success('已复制到剪贴板')
  })
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
    default: return difficulty || '未知'
  }
}

const statusTagType = (status: string) => {
  switch (status) {
    case 'ACCEPTED': return 'success'
    case 'WRONG_ANSWER': return 'danger'
    case 'TIMEOUT': return 'warning'
    default: return 'info'
  }
}

onMounted(() => {
  loadQuestion()
})
</script>

<style scoped>
.question-detail-container {
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
.header h1 {
  margin: 0;
  font-size: 20px;
  color: #2d3748;
}

.content {
  max-width: 1000px;
  margin: 0 auto;
}

.question-info {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.question-title {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
}

.section {
  margin-top: 16px;
}
.section h3 {
  font-size: 15px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
}
.description {
  line-height: 1.8;
  font-size: 15px;
  color: #2d3748;
  background-color: #f7fafc;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.sql-block-wrapper {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  background-color: #1e293b;
}
.sql-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 16px;
  background-color: #0f172a;
  border-bottom: 1px solid #334155;
}
.sql-lang {
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
}
.sql-toolbar .el-button {
  color: #94a3b8;
  font-size: 12px;
}
.sql-toolbar .el-button:hover {
  color: #e2e8f0;
}
.sql-block {
  margin: 0;
  padding: 16px;
  overflow-x: auto;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 13px;
  line-height: 1.6;
  color: #e2e8f0;
  background-color: #1e293b;
  white-space: pre-wrap;
  word-break: break-all;
}

.sample-row {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}
.sample-item {
  flex: 1;
}
.sample-item h3 {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 6px;
}
.sample {
  background-color: #f7fafc;
  padding: 12px;
  border-radius: 8px;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 13px;
  border: 1px solid #e2e8f0;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

.sql-editor {
  margin-bottom: 20px;
}
.sql-textarea :deep(textarea) {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 14px;
}
.actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}

.result {
  margin-top: 20px;
}
.result-content {
  padding: 4px 0;
}
.status {
  margin-bottom: 12px;
}
.score {
  margin-bottom: 12px;
}
.score-value {
  font-size: 28px;
  font-weight: 700;
  color: #409eff;
}
.details pre {
  background-color: #f7fafc;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 13px;
  border: 1px solid #e2e8f0;
}
</style>