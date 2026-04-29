<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter, RouterLink, RouterView } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const student = computed(() => userStore.studentInfo)

function logout() {
  userStore.clearUser()
  router.push('/login')
}
</script>

<template>
  <el-container>
    <el-header class="app-header" height="64px">
      <div class="left">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/grades">成绩查询</RouterLink>
      </div>
      <div class="right">
        <span v-if="student">{{ student.name }} </span>
        <el-button v-if="student" type="text" @click="logout">退出</el-button>
        <RouterLink v-else to="/login">登录</RouterLink>
      </div>
    </el-header>

    <main>
      <RouterView />
    </main>
  </el-container>
</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}
.left a,
.right a {
  margin-right: 16px;
  color: #fff;
}
.left a {
  color: #fff;
  font-weight: 600;
}

</style>
