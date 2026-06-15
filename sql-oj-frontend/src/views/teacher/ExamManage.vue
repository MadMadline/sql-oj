<template>
  <div class="exam-manage">
    <div class="header">
      <h1>📋 考试管理</h1>
      <el-button type="primary" @click="dialogVisible = true">+ 创建考试</el-button>
    </div>

    <el-table :data="exams" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="考试名称" />
      <el-table-column prop="start_time" label="开始时间" width="180" />
      <el-table-column prop="end_time" label="结束时间" width="180" />
      <el-table-column prop="total_score" label="总分" width="80" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="viewRanking(row.id)">排名</el-button>
          <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建考试弹窗 -->
    <el-dialog v-model="dialogVisible" title="创建考试" width="600px">
      <el-form :model="examForm" label-width="100px">
        <el-form-item label="考试名称" required>
          <el-input v-model="examForm.title" />
        </el-form-item>
        <el-form-item label="开始时间" required>
          <el-date-picker
            v-model="examForm.start_time"
            type="datetime"
            placeholder="选择日期时间"
            value-format="YYYY-MM-DDTHH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="结束时间" required>
          <el-date-picker
            v-model="examForm.end_time"
            type="datetime"
            placeholder="选择日期时间"
            value-format="YYYY-MM-DDTHH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="总分" required>
          <el-input-number v-model="examForm.total_score" :min="0" />
        </el-form-item>
        <el-form-item label="选择题目">
          <div v-for="q in selectedQuestions" :key="q.id" class="question-item">
            <span>{{ q.description }}</span>
            <el-input-number v-model="q.score" :min="0" :max="100" size="small" style="width: 100px" />
            <el-button type="danger" size="small" @click="removeQuestion(q.id)">移除</el-button>
          </div>
          <el-select v-model="selectedQuestionId" placeholder="添加题目" @change="addQuestion">
            <el-option
              v-for="q in availableQuestions"
              :key="q.id"
              :label="q.description"
              :value="q.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createExam">创建</el-button>
      </template>
    </el-dialog>

    <!-- 排名弹窗 -->
    <el-dialog v-model="rankVisible" :title="`考试成绩排名 - ${currentExamTitle}`" width="600px">
      <el-table :data="rankings" stripe>
        <el-table-column prop="rank" label="排名" width="70" />
        <el-table-column prop="student_name" label="学生" />
        <el-table-column prop="score" label="得分" />
        <el-table-column prop="submitted_at" label="提交时间" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getExams, createExam, deleteExam, getExamResult } from '../../api/exams'
import { getQuestions } from '../../api/questions'

const loading = ref(false)
const dialogVisible = ref(false)
const rankVisible = ref(false)
const exams = ref<any[]>([])
const allQuestions = ref<any[]>([])
const rankings = ref<any[]>([])
const currentExamTitle = ref('')

const examForm = ref({
  title: '',
  start_time: '',
  end_time: '',
  total_score: 100
})

const selectedQuestions = ref<{ id: number; description: string; score: number }[]>([])
const selectedQuestionId = ref<number | null>(null)

const availableQuestions = computed(() => {
  return allQuestions.value.filter(q => !selectedQuestions.value.some(sq => sq.id === q.id))
})

const loadExams = async () => {
  loading.value = true
  try {
    const res = await getExams()
    exams.value = res.data.results || res.data
  } catch (error) {
    ElMessage.error('加载考试列表失败')
  } finally {
    loading.value = false
  }
}

const loadQuestions = async () => {
  try {
    const res = await getQuestions()
    allQuestions.value = res.data.results || res.data
  } catch (error) {
    ElMessage.error('加载题目列表失败')
  }
}

const addQuestion = () => {
  if (!selectedQuestionId.value) return
  const question = allQuestions.value.find(q => q.id === selectedQuestionId.value)
  if (question) {
    selectedQuestions.value.push({
      id: question.id,
      description: question.description,
      score: 10
    })
  }
  selectedQuestionId.value = null
}

const removeQuestion = (id: number) => {
  selectedQuestions.value = selectedQuestions.value.filter(q => q.id !== id)
}

const createExam = async () => {
  if (!examForm.value.title) {
    ElMessage.warning('请填写考试名称')
    return
  }

  try {
    await createExam({
      title: examForm.value.title,
      start_time: examForm.value.start_time,
      end_time: examForm.value.end_time,
      total_score: examForm.value.total_score,
      exam_questions: selectedQuestions.value.map(q => ({
        question: q.id,
        score: q.score
      }))
    })
    ElMessage.success('创建成功')
    dialogVisible.value = false
    loadExams()
    // 重置表单
    examForm.value = { title: '', start_time: '', end_time: '', total_score: 100 }
    selectedQuestions.value = []
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const viewRanking = async (examId: number) => {
  try {
    const res = await getExamResult(examId)
    const exam = exams.value.find(e => e.id === examId)
    currentExamTitle.value = exam?.title || ''
    rankings.value = res.data.results || res.data
    rankVisible.value = true
  } catch (error) {
    ElMessage.error('加载排名失败')
  }
}

const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定删除此考试？', '提示').then(async () => {
    try {
      await deleteExam(id)
      ElMessage.success('删除成功')
      loadExams()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

onMounted(() => {
  loadExams()
  loadQuestions()
})
</script>

<script lang="ts">
import { computed } from 'vue'
export default {}
</script>

<style scoped>
.exam-manage {
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
.question-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
}
</style>