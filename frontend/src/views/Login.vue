<template>
  <div class="login-page">
    <div class="orb orb-1" />
    <div class="orb orb-2" />
    <div class="login-shell">
      <section class="brand-panel">
        <div class="brand-badge">SE</div>
        <p class="brand-kicker">Student Score Query</p>
        <h1 class="brand-title">学生成绩查询系统</h1>
        <p class="brand-desc">
          一站式查询成绩、学分与绩点。注册后即可快速查看学业进展。
        </p>
        <div class="brand-tags">
          <span>安全登录</span>
          <span>实时查询</span>
          <span>清晰报表</span>
        </div>
      </section>
      <section class="form-panel">
        <header class="form-header">
          <h2>{{ mode === 'login' ? '欢迎回来' : '创建账号' }}</h2>
          <p>{{ mode === 'login' ? '请输入学号与密码登录系统' : '填写信息快速完成注册' }}</p>
          <div class="mode-switch">
            <button
              class="mode-btn"
              :class="{ active: mode === 'login' }"
              type="button"
              @click="switchMode('login')"
            >
              登录
            </button>
            <button
              class="mode-btn"
              :class="{ active: mode === 'register' }"
              type="button"
              @click="switchMode('register')"
            >
              注册
            </button>
          </div>
        </header>

        <el-form
          v-if="mode === 'login'"
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-width="80px"
        >
          <el-form-item label="学号" prop="studentId">
            <el-input v-model="loginForm.studentId" placeholder="请输入学号" clearable />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" class="submit-btn" @click="handleLogin" :loading="loginLoading">
              登录
            </el-button>
          </el-form-item>
        </el-form>

        <el-form
          v-else
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          label-width="80px"
        >
          <el-form-item label="学号" prop="studentId">
            <el-input v-model="registerForm.studentId" placeholder="请输入学号" clearable />
          </el-form-item>
          <el-form-item label="姓名" prop="name">
            <el-input v-model="registerForm.name" placeholder="请输入姓名" clearable />
          </el-form-item>
          <el-form-item label="专业" prop="major">
            <el-input v-model="registerForm.major" placeholder="如：软件工程" clearable />
          </el-form-item>
          <el-form-item label="年级" prop="grade">
            <el-input v-model="registerForm.grade" placeholder="如：2023级" clearable />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" show-password />
          </el-form-item>
          <el-form-item label="确认" prop="confirmPassword">
            <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" class="submit-btn" @click="handleRegister" :loading="registerLoading">
              注册并进入系统
            </el-button>
          </el-form-item>
        </el-form>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: 'LoginView' })
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { loginApi, registerApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
type Mode = 'login' | 'register'

const mode = ref<Mode>('login')
const loginFormRef = ref<FormInstance>()
const registerFormRef = ref<FormInstance>()
const loginLoading = ref(false)
const registerLoading = ref(false)

const loginForm = reactive({
  studentId: '',
  password: ''
})

const registerForm = reactive({
  studentId: '',
  name: '',
  major: '',
  grade: '',
  password: '',
  confirmPassword: ''
})

const loginRules: FormRules = {
  studentId: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const registerRules: FormRules = {
  studentId: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次密码不一致'))
          return
        }
        callback()
      },
      trigger: 'blur'
    }
  ]
}

const switchMode = (nextMode: Mode) => {
  if (mode.value === nextMode) return
  mode.value = nextMode
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    loginLoading.value = true
    try {
      const res = await loginApi(loginForm)
      userStore.setUser(res.token, res.studentInfo)
      ElMessage.success('登录成功')
      router.push('/grades')
    } catch (err) {
      // 错误由拦截器处理
      console.debug(err)
    } finally {
      loginLoading.value = false
    }
  })
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return
    registerLoading.value = true
    try {
      const res = await registerApi({
        studentId: registerForm.studentId,
        name: registerForm.name,
        major: registerForm.major || undefined,
        grade: registerForm.grade || undefined,
        password: registerForm.password
      })
      userStore.setUser(res.token, res.studentInfo)
      ElMessage.success('注册成功')
      router.push('/grades')
    } catch (err) {
      // 错误由拦截器处理
      console.debug(err)
    } finally {
      registerLoading.value = false
    }
  })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=ZCOOL+XiaoWei&display=swap');

.login-page {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(circle at top, rgba(255, 235, 204, 0.8), transparent 55%),
    linear-gradient(120deg, #f6f3ef 0%, #eef3f7 45%, #f7faf5 100%);
  font-family: 'Space Grotesk', 'Noto Sans SC', sans-serif;
  overflow: hidden;
  z-index: 50;
}

.orb {
  position: absolute;
  border-radius: 999px;
  filter: blur(0);
  opacity: 0.7;
}

.orb-1 {
  width: 320px;
  height: 320px;
  background: radial-gradient(circle, rgba(46, 196, 182, 0.45), transparent 70%);
  top: -90px;
  left: -60px;
}

.orb-2 {
  width: 240px;
  height: 240px;
  background: radial-gradient(circle, rgba(244, 162, 97, 0.55), transparent 70%);
  bottom: -80px;
  right: -30px;
}

.login-shell {
  width: min(980px, 94vw);
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 32px;
  padding: 32px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.12);
  backdrop-filter: blur(14px);
  position: relative;
  z-index: 1;
}

.brand-panel {
  padding: 24px 18px 24px 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.brand-badge {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  font-weight: 700;
  color: #102a43;
  background: linear-gradient(135deg, #2ec4b6, #8ecae6);
  box-shadow: 0 10px 20px rgba(46, 196, 182, 0.35);
}

.brand-kicker {
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 12px;
  color: #6b7a90;
}

.brand-title {
  margin: 0;
  font-family: 'ZCOOL XiaoWei', serif;
  font-size: 34px;
  color: #102a43;
}

.brand-desc {
  margin: 0;
  color: #52606d;
  font-size: 15px;
  line-height: 1.6;
}

.brand-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.brand-tags span {
  padding: 6px 12px;
  border-radius: 999px;
  background: #f0f4f8;
  color: #334e68;
  font-size: 12px;
}

.form-panel {
  background: #ffffff;
  border-radius: 22px;
  padding: 26px;
  border: 1px solid #e6edf5;
}

.form-header {
  margin-bottom: 18px;
}

.form-header h2 {
  margin: 0 0 6px;
  color: #102a43;
  font-size: 24px;
}

.form-header p {
  margin: 0 0 16px;
  color: #6b7a90;
  font-size: 14px;
}

.mode-switch {
  display: inline-flex;
  gap: 8px;
  background: #f1f5f9;
  padding: 6px;
  border-radius: 999px;
}

.mode-btn {
  border: none;
  background: transparent;
  padding: 6px 16px;
  border-radius: 999px;
  font-size: 13px;
  color: #52606d;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mode-btn.active {
  background: #102a43;
  color: #fff;
  box-shadow: 0 6px 16px rgba(16, 42, 67, 0.2);
}

.submit-btn {
  width: 100%;
  height: 42px;
  font-weight: 600;
}

@media (max-width: 860px) {
  .login-shell {
    grid-template-columns: 1fr;
    padding: 22px;
  }

  .brand-panel {
    padding: 0;
  }
}
</style>
