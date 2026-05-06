from mappers.base_mapper import BaseMapper


class StudentMapper(BaseMapper):
    @classmethod
    async def find_by_student_id(cls, student_id):
        sql = """
            SELECT student_id, name, password_hash, major, grade
            FROM students
            WHERE student_id = %s
        """
        return await cls.execute_one(sql, (student_id,))

    @classmethod
    async def verify_password(cls, student_id, password_hash):
        sql = """
            SELECT student_id, name, major, grade
            FROM students
            WHERE student_id = %s AND password_hash = %s
        """
        return await cls.execute_one(sql, (student_id, password_hash))

    @classmethod
    async def create_student(cls, student_id, name, password_hash, major=None, grade=None):
        sql = """
            INSERT INTO students (student_id, name, password_hash, major, grade)
            VALUES (%s, %s, %s, %s, %s)
        """
        return await cls.execute_update(sql, (student_id, name, password_hash, major, grade))
