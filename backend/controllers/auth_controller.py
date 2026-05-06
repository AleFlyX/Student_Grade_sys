from sanic import json
from sanic.views import HTTPMethodView

from services.auth_service import AuthService


class LoginView(HTTPMethodView):
    async def post(self, request):
        try:
            data = request.json or {}
            student_id = data.get("studentId")
            password = data.get("password")

            if not student_id or not password:
                return json({
                    "code": 400,
                    "message": "学号和密码不能为空",
                    "data": None,
                }, status=400)

            result, error = await AuthService.login(student_id, password)
            if error:
                return json({
                    "code": 401,
                    "message": error,
                    "data": None,
                }, status=401)

            return json({
                "code": 200,
                "message": "登录成功",
                "data": result,
            })
        except Exception as exc:
            return json({
                "code": 500,
                "message": f"服务器错误: {str(exc)}",
                "data": None,
            }, status=500)


class RegisterView(HTTPMethodView):
    async def post(self, request):
        try:
            data = request.json or {}
            student_id = data.get("studentId")
            name = data.get("name")
            password = data.get("password")
            major = data.get("major")
            grade = data.get("grade")

            if not student_id or not name or not password:
                return json({
                    "code": 400,
                    "message": "学号、姓名和密码不能为空",
                    "data": None,
                }, status=400)

            result, error = await AuthService.register(student_id, name, password, major, grade)
            if error:
                return json({
                    "code": 409,
                    "message": error,
                    "data": None,
                }, status=409)

            return json({
                "code": 200,
                "message": "注册成功",
                "data": result,
            })
        except Exception as exc:
            return json({
                "code": 500,
                "message": f"服务器错误: {str(exc)}",
                "data": None,
            }, status=500)
