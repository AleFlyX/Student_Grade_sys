from config import Config
from mappers.grade_mapper import GradeMapper


class GradeService:
    @staticmethod
    def calculate_grade_point(score):
        for threshold, gpa in Config.GPA_RULES:
            if score >= threshold:
                return gpa
        return 0.0

    @classmethod
    async def get_student_grades(cls, student_id, academic_year=None, semester=None):
        grades_db = await GradeMapper.find_grades_by_student(student_id, academic_year, semester)
        if not grades_db:
            return None

        grades = []
        total_credit = 0.0
        total_grade_points = 0.0

        for row in grades_db:
            score = float(row["score"])
            credit = float(row["credit"])
            grade_point = cls.calculate_grade_point(score)

            grades.append({
                "courseId": row["course_id"],
                "courseName": row["course_name"],
                "credit": credit,
                "courseNature": row["course_nature"],
                "academicYear": row["academic_year"],
                "semester": row["semester"],
                "score": score,
                "gradePoint": grade_point,
                "status": row["status"],
            })

            total_credit += credit
            total_grade_points += grade_point * credit

        gpa = round(total_grade_points / total_credit, 2) if total_credit > 0 else 0.0

        return {
            "studentId": student_id,
            "name": "",
            "grades": grades,
            "summary": {
                "totalCredit": round(total_credit, 1),
                "gpa": gpa,
            },
        }
