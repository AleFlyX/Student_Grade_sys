from mappers.student_mapper import StudentMapper
from utils.jwt_util import JWTUtil
from utils.password_util import PasswordUtil


class AuthService:
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
