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
    async def find_profile_by_student_id(cls, student_id):
        sql = """
            SELECT student_id, name, major, grade
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

    @classmethod
    async def update_password(cls, student_id, password_hash):
        sql = """
            UPDATE students
            SET password_hash = %s
            WHERE student_id = %s
        """
        return await cls.execute_update(sql, (password_hash, student_id))

    @classmethod
    async def update_profile(cls, student_id, name, major=None, grade=None):
        sql = """
            UPDATE students
            SET name = %s, major = %s, grade = %s
            WHERE student_id = %s
        """
        return await cls.execute_update(sql, (name, major, grade, student_id))
