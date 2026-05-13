<template>
  <div class="grade-container">
    <el-header class="header">
      <div class="user-info">
        <span>欢迎，{{ studentInfo?.name }} ({{ studentInfo?.studentId }})</span>
        <span>{{ studentInfo?.major }} | {{ studentInfo?.grade }}</span>
      </div>
      <el-button type="danger" plain @click="logout">退出登录</el-button>
    </el-header>

    <el-main>
      <el-card class="filter-card" >
        <el-form :inline="true" :model="queryParams" >
          <el-form-item label="学年" class="filter-card-item">
            <el-select v-model="queryParams.academicYear" clearable placeholder="请选择学年">
              <el-option label="2024-2025" value="2024-2025" />
              <el-option label="2023-2024" value="2023-2024" />
            </el-select>
          </el-form-item>
          <el-form-item label="学期" class="filter-card-item">
            <el-select v-model="queryParams.semester" clearable placeholder="请选择学期">
              <el-option label="秋季" value="AUTUMN" />
              <el-option label="春季" value="SPRING" />
              <el-option label="夏季" value="SUMMER" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchGrades" :loading="loading">查询</el-button>
            <el-button @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-row :gutter="20" class="summary-row">
        <el-col :span="12">
          <el-card shadow="hover">
            <div class="summary-item">
              <div class="summary-label">总学分</div>
              <div class="summary-value">{{ gradeData?.summary.totalCredit || 0 }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover">
            <div class="summary-item">
              <div class="summary-label">平均绩点 (GPA)</div>
              <div class="summary-value">{{ gradeData?.summary.gpa || 0 }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-card class="grade-table-card">
        <template #header>
          <span>课程成绩列表</span>
        </template>
        <el-table :data="gradeData?.grades || []" stripe border>
          <el-table-column prop="courseId" label="课程编号" width="120" />
          <el-table-column prop="courseName" label="课程名称" min-width="150" />
          <el-table-column prop="credit" label="学分" width="80" />
          <el-table-column prop="courseNature" label="性质" width="80" />
          <el-table-column prop="academicYear" label="学年" width="100" />
          <el-table-column prop="semester" label="学期" width="80">
            <template #default="{ row }">
              {{ semesterMap[row.semester] }}
            </template>
          </el-table-column>
          <el-table-column prop="score" label="成绩" width="80">
            <template #default="{ row }">
              <span :style="{ color: row.score < 60 ? 'red' : 'inherit' }">{{ row.score }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="gradePoint" label="绩点" width="80" />
          <el-table-column prop="status" label="状态" width="80" />
        </el-table>
        <el-empty v-if="!gradeData?.grades?.length" description="暂无成绩数据" />
      </el-card>
    </el-main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { getCurrentStudentApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'
import { getGradesApi, type GradeQueryParams } from '@/api/grade'
import type { GradeData } from '@/types/grade'

const router = useRouter()
const userStore = useUserStore()
const studentInfo = computed(() => userStore.studentInfo)

const loading = ref(false)
const gradeData = ref<GradeData | null>(null)
const queryParams = ref<GradeQueryParams>({ academicYear: undefined, semester: undefined })

const semesterMap: Record<string, string> = { AUTUMN: '秋季', SPRING: '春季', SUMMER: '夏季' }

const fetchGrades = async () => {
  loading.value = true
  try {
    const data = await getGradesApi(queryParams.value)
    gradeData.value = data
  } catch {
    gradeData.value = null
  } finally {
    loading.value = false
  }
}

const resetQuery = () => {
  queryParams.value = { academicYear: undefined, semester: undefined }
  fetchGrades()
}

const logout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' })
    .then(() => {
      userStore.clearUser()
      router.push('/login')
    })
    .catch(() => {})
}

const loadProfile = async () => {
  try {
    const data = await getCurrentStudentApi()
    userStore.setStudentInfo(data.studentInfo)
  } catch {
  }
}

onMounted(() => {
  if (!userStore.studentInfo) {
    loadProfile()
  }
  fetchGrades()
})
</script>

<style scoped>
.grade-container {
  min-height: 100vh;
  background: #f0f2f5;
}
.header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}
.user-info {
  display: flex;
  gap: 20px;
  font-size: 16px;
}
.filter-card { margin-bottom: 20px; width: 100%; display: flex; flex-wrap: wrap; gap: 20px; }
.filter-card-item{
  flex: 1;
  min-width: 200px;
}
.summary-row { margin-bottom: 20px; }
.summary-item { text-align: center; }
.summary-label { font-size: 14px; color: #909399; margin-bottom: 10px; }
.summary-value { font-size: 32px; font-weight: bold; color: #409eff; }
.grade-table-card { margin-top: 20px; }
</style>
