<template>
  <div class="create-container">
    <div class="header">
      <el-button @click="goBack">← 返回</el-button>
      <h1>{{ isEdit ? '编辑题目' : '创建题目' }}</h1>
    </div>

    <el-form :model="form" label-width="120px" v-loading="loading">
      <el-form-item label="题目描述" required>
        <el-input v-model="form.description" type="textarea" :rows="3" />
      </el-form-item>

      <el-form-item label="难度" required>
        <el-radio-group v-model="form.difficulty">
          <el-radio value="easy">简单</el-radio>
          <el-radio value="medium">中等</el-radio>
          <el-radio value="hard">困难</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="建表语句">
        <el-input v-model="form.create_table_sql" type="textarea" :rows="5" placeholder="CREATE TABLE ..." />
      </el-form-item>

      <el-form-item label="样例输入">
        <el-input v-model="form.sample_input" type="textarea" :rows="2" />
      </el-form-item>

      <el-form-item label="样例输出">
        <el-input v-model="form.sample_output" type="textarea" :rows="2" />
      </el-form-item>

      <el-form-item label="正确答案 SQL">
        <el-input v-model="form.correct_sql" type="textarea" :rows="3" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
        <el-button @click="goBack">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isEdit = ref(false)
const loading = ref(false)

const form = ref({
  description: '',
  difficulty: 'easy',
  create_table_sql: '',
  sample_input: '',
  sample_output: '',
  correct_sql: ''
})

const loadQuestion = async (id: number) => {
  // TODO: 调用获取题目详情 API
  // 编辑模式时加载已有数据
}

const handleSubmit = async () => {
  if (!form.value.description) {
    ElMessage.warning('请填写题目描述')
    return
  }

  loading.value = true
  try {
    if (isEdit.value) {
      // TODO: 调用编辑 API
      ElMessage.success('编辑成功')
    } else {
      // TODO: 调用创建 API
      ElMessage.success('创建成功')
    }
    router.push('/teacher/questions')
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/teacher/questions')
}

onMounted(() => {
  const id = route.query.id
  if (id) {
    isEdit.value = true
    loadQuestion(Number(id))
  }
})
</script>

<style scoped>
.create-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}
.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}
</style>