import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/token'

const routes = [
  {
    path: '/',
    redirect: '/grades',
    meta: { requiresAuth: false },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/public/login/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/grades',
    name: 'GradeQuery',
    component: () => import('@/views/main/grade/GradeQuery.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'StudentCenter',
    component: () => import('@/views/main/student/StudentCenter.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = getToken()
  const meta = to.meta as { requiresAuth?: boolean }
  if (meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/grades')
  } else {
    next()
  }
})

export default router
