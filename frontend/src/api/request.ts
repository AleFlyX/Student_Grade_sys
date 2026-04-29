import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import { getToken, removeToken } from '@/utils/token'

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

class Request {
  private instance: AxiosInstance

  constructor(baseURL: string) {
    this.instance = axios.create({
      baseURL,
      timeout: 10000,
      headers: { 'Content-Type': 'application/json' }
    })

    this.instance.interceptors.request.use((config: InternalAxiosRequestConfig) => {
      const token = getToken()
      if (token && config.headers) (config.headers as any).Authorization = `Bearer ${token}`
      return config
    })

    this.instance.interceptors.response.use(
      (response: AxiosResponse<ApiResponse>) => {
        const res = response.data
        if (res.code === 200 || res.code === 0) {
          return res.data
        } else if (res.code === 401) {
          removeToken()
          window.location.href = '/login'
          return Promise.reject(new Error(res.message))
        } else {
          ElMessage.error(res.message || '请求失败')
          return Promise.reject(new Error(res.message))
        }
      },
      (error: any) => {
        ElMessage.error(error.message || '网络错误')
        return Promise.reject(error)
      }
    )
  }

  public get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.get(url, config)
  }

  public post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.post(url, data, config)
  }
}

export default new Request(import.meta.env.VITE_API_BASE_URL || '/api')
