from sanic import json

from utils.jwt_util import JWTUtil


async def auth_middleware(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return json({
            "code": 401,
            "message": "未提供认证信息",
            "data": None,
        }, status=401)

    token = auth_header.split(" ", 1)[1].strip()
    payload, error = JWTUtil.verify_token(token)
    if error:
        return json({
            "code": 401,
            "message": error,
            "data": None,
        }, status=401)

    request.ctx.student_info = payload
    return None
