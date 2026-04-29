import request from './request'
import type { LoginParams, LoginResponse } from '@/types/auth'

export const loginApi = (data: LoginParams): Promise<LoginResponse> => {
  return request.post('/auth/login', data)
}
