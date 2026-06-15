<template>
  <div class="container">
    <h1>题目详情页</h1>
    <p>题目 ID: {{ questionId }}</p>
    <el-button @click="goBack">返回列表</el-button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const questionId = computed(() => route.params.id)

const goBack = () => {
  router.push('/questions')
}
</script>

<style scoped>
.container {
  padding: 20px;
}
</style>