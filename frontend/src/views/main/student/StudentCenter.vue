<template>
  <div class="student-center-page">
    <section class="hero-card">
      <div>
        <p class="eyebrow">Student Center</p>
        <h1>学生中心</h1>
        <p class="subtext">
          查看个人信息，修改密码，并作为第一阶段的账户管理入口。
        </p>
      </div>
      <el-button type="primary" plain @click="goGrades">返回成绩查询</el-button>
    </section>

    <el-row :gutter="20" class="profile-grid">
      <el-col :xs="24" :lg="10">
        <el-card id="profile-info" class="panel" shadow="never">
          <template #header>
            <div class="panel-header">
              <span>个人信息</span>
              <el-tag type="success">已登录</el-tag>
            </div>
          </template>

          <div class="profile-list">
            <div class="profile-item">
              <span class="label">学号</span>
              <span class="value">{{ profile.studentId }}</span>
            </div>
            <div class="profile-item">
              <span class="label">姓名</span>
              <span class="value">{{ profile.name }}</span>
            </div>
            <div class="profile-item">
              <span class="label">专业</span>
              <span class="value">{{ profile.major || '未填写' }}</span>
            </div>
            <div class="profile-item">
              <span class="label">年级</span>
              <span class="value">{{ profile.grade || '未填写' }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="14">
        <el-card id="profile-edit" class="panel" shadow="never">
          <template #header>
            <div class="panel-header">
              <span>修改个人信息</span>
            </div>
          </template>

          <el-form ref="profileFormRef" :model="profileForm" :rules="profileRules" label-width="90px">
            <el-form-item label="学号">
              <el-input :model-value="profileForm.studentId" disabled />
            </el-form-item>
            <el-form-item label="姓名" prop="name">
              <el-input v-model="profileForm.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="专业" prop="major">
              <el-input v-model="profileForm.major" placeholder="请输入专业" />
            </el-form-item>
            <el-form-item label="年级" prop="grade">
              <el-input v-model="profileForm.grade" placeholder="例如：2023级" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="profileSaving" @click="submitProfileChange">保存信息</el-button>
              <el-button @click="resetProfileForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="14">
        <el-card class="panel password-panel" shadow="never">
          <template #header>
            <div class="panel-header">
              <span>修改密码</span>
            </div>
          </template>

          <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="90px">
            <el-form-item label="原密码" prop="oldPassword">
              <el-input v-model="passwordForm.oldPassword" type="password" show-password placeholder="请输入原密码" />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="至少8位，含字母和数字" />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="再次输入新密码" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="submitPasswordChange">保存修改</el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { changePasswordApi, getCurrentStudentApi, updateStudentProfileApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const profile = computed(() => userStore.studentInfo ?? { studentId: '', name: '', major: '', grade: '' })

const profileFormRef = ref<FormInstance>()
const profileSaving = ref(false)
const profileForm = reactive({
  studentId: '',
  name: '',
  major: '',
  grade: '',
})

const passwordFormRef = ref<FormInstance>()
const saving = ref(false)
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const passwordRules: FormRules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8位', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        const hasLetter = /[a-zA-Z]/.test(value || '')
        const hasDigit = /\d/.test(value || '')
        if (!hasLetter || !hasDigit) {
          callback(new Error('密码需同时包含字母和数字'))
          return
        }
        callback()
      },
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的新密码不一致'))
          return
        }
        callback()
      },
      trigger: 'blur'
    }
  ]
}

const profileRules: FormRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
}

const loadProfile = async () => {
  try {
    const data = await getCurrentStudentApi()
    userStore.setStudentInfo(data.studentInfo)
  } catch (error) {
    console.debug(error)
  }
}

const syncProfileForm = () => {
  profileForm.studentId = profile.value.studentId
  profileForm.name = profile.value.name
  profileForm.major = profile.value.major
  profileForm.grade = profile.value.grade
}

const submitProfileChange = async () => {
  if (!profileFormRef.value) return
  await profileFormRef.value.validate(async (valid) => {
    if (!valid) return
    profileSaving.value = true
    try {
      const data = await updateStudentProfileApi({
        studentId: profileForm.studentId,
        name: profileForm.name,
        major: profileForm.major,
        grade: profileForm.grade,
      })
      userStore.setStudentInfo(data.studentInfo)
      ElMessage.success('个人信息更新成功')
    } finally {
      profileSaving.value = false
    }
  })
}

const resetProfileForm = () => {
  syncProfileForm()
}

const submitPasswordChange = async () => {
  if (!passwordFormRef.value) return
  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return
    saving.value = true
    try {
      await changePasswordApi({
        oldPassword: passwordForm.oldPassword,
        newPassword: passwordForm.newPassword,
      })
      ElMessage.success('密码修改成功，请使用新密码重新登录')
      userStore.clearUser()
      router.push('/login')
    } finally {
      saving.value = false
    }
  })
}

const resetForm = () => {
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
}

const goGrades = () => {
  router.push('/grades')
}

watch(
  profile,
  () => {
    syncProfileForm()
  },
  { immediate: true }
)

onMounted(() => {
  if (!userStore.studentInfo) {
    loadProfile()
  }
  if (route.hash) {
    nextTick(() => {
      const element = document.querySelector(route.hash)
      element?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }
})
</script>

<style scoped>
.student-center-page {
  min-height: calc(100vh - 64px);
  padding: 24px;
  background:
    radial-gradient(circle at top right, rgba(46, 196, 182, 0.18), transparent 35%),
    linear-gradient(180deg, #f7fafc 0%, #eef4f8 100%);
}

.hero-card {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  padding: 28px;
  margin-bottom: 20px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
}

.eyebrow {
  margin: 0 0 8px;
  color: #7c8aa0;
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.hero-card h1 {
  margin: 0;
  color: #102a43;
  font-size: 30px;
}

.subtext {
  margin: 10px 0 0;
  color: #52606d;
}

.profile-grid {
  align-items: stretch;
}

.panel {
  border-radius: 20px;
  min-height: 100%;
}

.password-panel {
  margin-top: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-list {
  display: grid;
  gap: 14px;
}

.profile-item {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 14px 16px;
  border-radius: 14px;
  background: #f8fbfd;
}

.label {
  color: #7c8aa0;
}

.value {
  color: #102a43;
  font-weight: 600;
}

@media (max-width: 768px) {
  .student-center-page {
    padding: 16px;
  }

  .hero-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .profile-item {
    flex-direction: column;
    gap: 6px;
  }
}
</style>
