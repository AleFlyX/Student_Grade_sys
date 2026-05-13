<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter, RouterView } from 'vue-router'
import { logoutApi } from '@/api/auth'
import Layout from '@/layouts/index.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const student = computed(() => userStore.studentInfo)
const showLayout = computed(() => route.meta.requiresAuth !== false && route.path !== '/login')

async function logout() {
  try {
    await logoutApi()
  } catch {
    // token 失效时直接本地清理即可
  }
  userStore.clearUser()
  router.push('/login')
}
</script>

<template>
  <Layout v-if="showLayout" />
  <RouterView v-else />
</template>
