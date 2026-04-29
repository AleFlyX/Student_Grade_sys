from sanic import json
from sanic.views import HTTPMethodView

from services.grade_service import GradeService


class GradeQueryView(HTTPMethodView):
    async def get(self, request):
        try:
            student_info = getattr(request.ctx, "student_info", None)
            if not student_info:
                return json({
                    "code": 401,
                    "message": "未提供认证信息",
                    "data": None,
                }, status=401)

            student_id = student_info.get("student_id")
            student_name = student_info.get("name", "")

            academic_year = request.args.get("academicYear")
            semester = request.args.get("semester")

            if semester and semester not in ["AUTUMN", "SPRING", "SUMMER"]:
                return json({
                    "code": 400,
                    "message": "semester参数值无效，允许值：AUTUMN, SPRING, SUMMER",
                    "data": None,
                }, status=400)

            result = await GradeService.get_student_grades(student_id, academic_year, semester)
            if not result:
                return json({
                    "code": 404,
                    "message": "未查询到成绩数据",
                    "data": None,
                }, status=404)

            result["name"] = student_name
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
