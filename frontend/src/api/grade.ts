import request from './request'
import type { GradeData } from '@/types/grade'

export interface GradeQueryParams {
  academicYear?: string
  semester?: 'AUTUMN' | 'SPRING' | 'SUMMER'
}

export const getGradesApi = (params?: GradeQueryParams): Promise<GradeData> => {
  return request.get('/grades', { params })
}
