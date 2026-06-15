<template>
  <div class="teacher-layout">
    <div class="sidebar">
      <div class="logo">
        <h2>SQL OJ</h2>
        <p>教师端</p>
      </div>
      <el-menu :default-active="activeMenu" router>
        <el-menu-item index="/teacher/questions">
          <el-icon><Document /></el-icon>
          <span>题目管理</span>
        </el-menu-item>
        <el-menu-item index="/teacher/exams">
          <el-icon><Notebook /></el-icon>
          <span>考试管理</span>
        </el-menu-item>
        <el-menu-item index="/teacher/stats">
          <el-icon><DataAnalysis /></el-icon>
          <span>统计分析</span>
        </el-menu-item>
      </el-menu>
      <div class="user-info">
        <span>{{ userStore.user?.username }}</span>
        <el-button type="danger" text @click="handleLogout">退出</el-button>
      </div>
    </div>
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Document, Notebook, DataAnalysis } from '@element-plus/icons-vue'
import { useUserStore } from '../../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
  ElMessage.success('已退出')
}
</script>

<style scoped>
.teacher-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 260px;
  background-color: #304156;
  color: #fff;
  display: flex;
  flex-direction: column;
}
.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #4a5a6e;
}
.logo h2 {
  margin: 0;
  color: #fff;
}
.logo p {
  margin: 5px 0 0;
  font-size: 12px;
  color: #a0b3c9;
}
.sidebar :deep(.el-menu) {
  flex: 1;
  border-right: none;
  background-color: #304156;
}
.sidebar :deep(.el-menu-item) {
  color: #bfcbd9;
}
.sidebar :deep(.el-menu-item.is-active) {
  color: #409eff;
  background-color: #263445;
}
.sidebar :deep(.el-menu-item:hover) {
  background-color: #263445;
}
.user-info {
  padding: 20px;
  border-top: 1px solid #4a5a6e;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #bfcbd9;
}
.main-content {
  flex: 1;
  background-color: #f0f2f5;
}
</style>