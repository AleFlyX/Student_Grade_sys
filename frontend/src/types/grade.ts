export interface GradeItem {
  courseId: string
  courseName: string
  credit: number
  courseNature: string
  academicYear: string
  semester: 'AUTUMN' | 'SPRING' | 'SUMMER'
  score: number
  gradePoint: number
  status: string
}

export interface GradeSummary {
  totalCredit: number
  gpa: number
}

export interface GradeData {
  studentId: string
  name: string
  grades: GradeItem[]
  summary: GradeSummary
}
