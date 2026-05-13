from sanic import json
from sanic.views import HTTPMethodView

from services.auth_service import AuthService


class StudentProfileView(HTTPMethodView):
    async def get(self, request):
        try:
            student_info = getattr(request.ctx, "student_info", None)
            if not student_info:
                return json({
                    "code": 401,
                    "message": "未提供认证信息",
                    "data": None,
                }, status=401)

            result, error = await AuthService.get_profile(student_info.get("student_id"))
            if error:
                return json({
                    "code": 404,
                    "message": error,
                    "data": None,
                }, status=404)

            return json({
                "code": 200,
                "message": "查询成功",
                "data": result,
            })
        except Exception as exc:
            return json({
                "code": 500,
                "message": f"服务器错误: {str(exc)}",
                "data": None,
            }, status=500)


class ChangePasswordView(HTTPMethodView):
    async def put(self, request):
        try:
            student_info = getattr(request.ctx, "student_info", None)
            if not student_info:
                return json({
                    "code": 401,
                    "message": "未提供认证信息",
                    "data": None,
                }, status=401)

            data = request.json or {}
            old_password = data.get("oldPassword")
            new_password = data.get("newPassword")

            if not old_password or not new_password:
                return json({
                    "code": 400,
                    "message": "原密码和新密码不能为空",
                    "data": None,
                }, status=400)

            result, error = await AuthService.change_password(
                student_info.get("student_id"),
                old_password,
                new_password,
            )
            if error:
                status_code = 400 if error in {"原密码错误", "密码长度至少为8位", "密码需同时包含字母和数字"} else 404
                return json({
                    "code": status_code,
                    "message": error,
                    "data": None,
                }, status=status_code)

            return json({
                "code": 200,
                "message": "密码修改成功",
                "data": result,
            })
        except Exception as exc:
            return json({
                "code": 500,
                "message": f"服务器错误: {str(exc)}",
                "data": None,
            }, status=500)


class UpdateProfileView(HTTPMethodView):
    async def put(self, request):
        try:
            student_info = getattr(request.ctx, "student_info", None)
            if not student_info:
                return json({
                    "code": 401,
                    "message": "未提供认证信息",
                    "data": None,
                }, status=401)

            data = request.json or {}
            name = data.get("name")
            major = data.get("major")
            grade = data.get("grade")

            result, error = await AuthService.update_profile(
                student_info.get("student_id"),
                name,
                major,
                grade,
            )
            if error:
                return json({
                    "code": 400,
                    "message": error,
                    "data": None,
                }, status=400)

            return json({
                "code": 200,
                "message": "个人信息更新成功",
                "data": result,
            })
        except Exception as exc:
            return json({
                "code": 500,
                "message": f"服务器错误: {str(exc)}",
                "data": None,
            }, status=500)


class LogoutView(HTTPMethodView):
    async def post(self, request):
        try:
            student_info = getattr(request.ctx, "student_info", None)
            if not student_info:
                return json({
                    "code": 401,
                    "message": "未提供认证信息",
                    "data": None,
                }, status=401)

            return json({
                "code": 200,
                "message": "退出成功",
                "data": {"success": True},
            })
        except Exception as exc:
            return json({
                "code": 500,
                "message": f"服务器错误: {str(exc)}",
                "data": None,
            }, status=500)