from mappers.base_mapper import BaseMapper


class GradeMapper(BaseMapper):
    @classmethod
    async def find_grades_by_student(cls, student_id, academic_year=None, semester=None):
        sql = """
            SELECT
                c.course_id, c.course_name, c.credit, c.course_nature,
                g.academic_year, g.semester, g.score, g.status
            FROM grades g
            JOIN courses c ON g.course_id = c.course_id
            WHERE g.student_id = %s
        """
        params = [student_id]

        if academic_year:
            sql += " AND g.academic_year = %s"
            params.append(academic_year)
        if semester:
            sql += " AND g.semester = %s"
            params.append(semester)

        sql += " ORDER BY g.academic_year DESC, g.semester"
        return await cls.execute_query(sql, tuple(params))

    @classmethod
    async def get_student_courses_count(cls, student_id):
        sql = """
            SELECT COUNT(*) AS count
            FROM grades
            WHERE student_id = %s
        """
        result = await cls.execute_one(sql, (student_id,))
        return result["count"] if result else 0
