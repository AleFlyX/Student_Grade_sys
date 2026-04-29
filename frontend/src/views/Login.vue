<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="title">学生成绩查询系统</h2>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="学号" prop="studentId">
          <el-input v-model="form.studentId" placeholder="请输入学号" clearable />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: 'LoginView' })
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { loginApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  studentId: '',
  password: ''
})

const rules: FormRules = {
  studentId: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const res = await loginApi(form)
      userStore.setUser(res.token, res.studentInfo)
      ElMessage.success('登录成功')
      router.push('/grades')
    } catch (err) {
      // 错误由拦截器处理
      console.debug(err)
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 50;
}
.login-card {
  width: 380px;
  padding: 20px;
}
.title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}
</style>
