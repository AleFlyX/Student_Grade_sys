import request from './request'
import type {
  ChangePasswordParams,
  LoginParams,
  LoginResponse,
  RegisterParams,
  RegisterResponse,
  StudentInfo,
} from '@/types/auth'

export const loginApi = (data: LoginParams): Promise<LoginResponse> => {
  return request.post('/auth/login', data)
}

export const registerApi = (data: RegisterParams): Promise<RegisterResponse> => {
  return request.post('/auth/register', data)
}

export const getCurrentStudentApi = (): Promise<{ studentInfo: StudentInfo }> => {
  return request.get('/students/me')
}

export const updateStudentProfileApi = (data: StudentInfo): Promise<{ studentInfo: StudentInfo }> => {
  return request.put('/students/me', data)
}

export const changePasswordApi = (data: ChangePasswordParams): Promise<{ success: boolean }> => {
  return request.put('/auth/change-password', data)
}

export const logoutApi = (): Promise<{ success: boolean }> => {
  return request.post('/auth/logout')
}
