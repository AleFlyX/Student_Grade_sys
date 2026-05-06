from mappers.student_mapper import StudentMapper
from utils.jwt_util import JWTUtil
from utils.password_util import PasswordUtil


class AuthService:
    @staticmethod
    def validate_password_strength(password):
        if len(password or "") < 8:
            return "密码长度至少为8位"

        has_letter = any(char.isalpha() for char in password)
        has_digit = any(char.isdigit() for char in password)
        if not has_letter or not has_digit:
            return "密码需同时包含字母和数字"

        return None

    @classmethod
    async def login(cls, student_id, password):
        password_hash = PasswordUtil.hash_password(password)
        student = await StudentMapper.verify_password(student_id, password_hash)

        if not student:
            return None, "学号或密码错误"

        token = JWTUtil.generate_token({
            "student_id": student["student_id"],
            "name": student["name"],
        })

        student_info = {
            "studentId": student["student_id"],
            "name": student["name"],
            "major": student.get("major"),
            "grade": student.get("grade"),
        }

        return {
            "token": token,
            "expiresIn": JWTUtil.EXPIRES,
            "studentInfo": student_info,
        }, None

    @classmethod
    async def register(cls, student_id, name, password, major=None, grade=None):
        existing = await StudentMapper.find_by_student_id(student_id)
        if existing:
            return None, "学号已存在"

        password_error = cls.validate_password_strength(password)
        if password_error:
            return None, password_error

        password_hash = PasswordUtil.hash_password(password)
        await StudentMapper.create_student(student_id, name, password_hash, major, grade)

        token = JWTUtil.generate_token({
            "student_id": student_id,
            "name": name,
        })

        student_info = {
            "studentId": student_id,
            "name": name,
            "major": major,
            "grade": grade,
        }

        return {
            "token": token,
            "expiresIn": JWTUtil.EXPIRES,
            "studentInfo": student_info,
        }, None

    @classmethod
    async def get_profile(cls, student_id):
        student = await StudentMapper.find_profile_by_student_id(student_id)
        if not student:
            return None, "学生不存在"

        return {
            "studentInfo": {
                "studentId": student["student_id"],
                "name": student["name"],
                "major": student.get("major"),
                "grade": student.get("grade"),
            }
        }, None

    @classmethod
    async def change_password(cls, student_id, old_password, new_password):
        student = await StudentMapper.find_by_student_id(student_id)
        if not student:
            return None, "学生不存在"

        if not PasswordUtil.verify_password(old_password, student["password_hash"]):
            return None, "原密码错误"

        password_error = cls.validate_password_strength(new_password)
        if password_error:
            return None, password_error

        new_password_hash = PasswordUtil.hash_password(new_password)
        await StudentMapper.update_password(student_id, new_password_hash)
        return {"success": True}, None
