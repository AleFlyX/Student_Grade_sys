import request from './request'
import type { LoginParams, LoginResponse, RegisterParams, RegisterResponse } from '@/types/auth'

export const loginApi = (data: LoginParams): Promise<LoginResponse> => {
  return request.post('/auth/login', data)
}

export const registerApi = (data: RegisterParams): Promise<RegisterResponse> => {
  return request.post('/auth/register', data)
}
