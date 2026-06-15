<template>
  <div class="login-container">
    <div class="login-card">
      <h2>SQL OJ 登录</h2>
      <div>
        <div>用户名：</div>
        <input v-model="form.username" placeholder="请输入用户名" />
      </div>
      <div>
        <div>密码：</div>
        <input v-model="form.password" type="password" placeholder="请输入密码" />
      </div>
      <div>
        <div>身份：</div>
        <label><input type="radio" value="student" v-model="form.user_type" /> 学生</label>
        <label><input type="radio" value="teacher" v-model="form.user_type" /> 教师</label>
      </div>
      <div style="margin-top: 20px;">
        <button @click="handleLogin">登录</button>
        <button @click="handleRegister">注册</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import { register } from '../api/auth'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  username: '',
  password: '',
  user_type: 'student' as 'student' | 'teacher'
})

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }

  try {
    await userStore.login(form.username, form.password)
    ElMessage.success('登录成功')

    // 根据身份跳转
    if (userStore.user?.user_type === 'teacher') {
      router.push('/teacher')
    } else {
      router.push('/questions')
    }
  } catch (error: any) {
    const msg = error.response?.data?.error || '登录失败'
    ElMessage.error(msg)
  }
}

const handleRegister = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }

  try {
    await register({
      username: form.username,
      email: `${form.username}@test.com`,
      password: form.password,
      user_type: form.user_type
    })
    ElMessage.success('注册成功，请登录')
  } catch (error: any) {
    const data = error.response?.data
    let msg = '注册失败'
    if (data?.username) msg = Array.isArray(data.username) ? data.username[0] : data.username
    else if (data?.password) msg = Array.isArray(data.password) ? data.password[0] : data.password
    else if (data?.error) msg = data.error
    ElMessage.error(msg)
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}
.login-card {
  width: 400px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}
input {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  box-sizing: border-box;
}
button {
  margin-right: 10px;
  padding: 8px 16px;
}
</style>