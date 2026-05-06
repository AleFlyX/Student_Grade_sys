export interface LoginParams {
  studentId: string
  password: string
}

export interface RegisterParams {
  studentId: string
  name: string
  password: string
  major?: string
  grade?: string
}

export interface StudentInfo {
  studentId: string
  name: string
  major: string
  grade: string
}

export interface LoginResponse {
  token: string
  expiresIn: number
  studentInfo: StudentInfo
}

export interface RegisterResponse extends LoginResponse {}
