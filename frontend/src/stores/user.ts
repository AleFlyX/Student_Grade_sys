import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { StudentInfo } from '@/types/auth'
import { getToken, setToken, removeToken } from '@/utils/token'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(getToken())
  const studentInfo = ref<StudentInfo | null>(null)

  const setUser = (newToken: string, info: StudentInfo) => {
    token.value = newToken
    studentInfo.value = info
    setToken(newToken)
  }

  const clearUser = () => {
    token.value = null
    studentInfo.value = null
    removeToken()
  }

  return { token, studentInfo, setUser, clearUser }
})
