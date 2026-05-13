from sanic import Sanic
from sanic.response import empty

from api.v1.auth import ChangePasswordView, LoginView, LogoutView, RegisterView
from api.v1.grade import GradeQueryView
from controllers.student_controller import StudentProfileView, UpdateProfileView
from mappers.base_mapper import BaseMapper
from middleware.auth_middleware import auth_middleware


app = Sanic("GradeSystem")


@app.listener("before_server_stop")
async def close_database_pool(app, loop):
    await BaseMapper.close_pool()


@app.middleware("response")
async def add_cors_headers(request, response):
    """添加 CORS 响应头"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Max-Age"] = "3600"


@app.options("/<path:path>")
async def handle_options(request, path):
    """处理 OPTIONS 预检请求"""
    return None


@app.middleware("request")
async def verify_token(request):
    if request.method == "OPTIONS":
        return empty(status=200)

    if request.path == "/api/auth/login":
        return None

    if request.path == "/api/auth/register":
        return None

    if request.path in {"/api/auth/logout", "/api/auth/change-password", "/api/students/me"}:
        return await auth_middleware(request)

    if request.path.startswith("/api/grades"):
        return await auth_middleware(request)

    return None


app.add_route(LoginView.as_view(), "/api/auth/login", methods=["POST"])
app.add_route(RegisterView.as_view(), "/api/auth/register", methods=["POST"])
app.add_route(LogoutView.as_view(), "/api/auth/logout", methods=["POST"])
app.add_route(ChangePasswordView.as_view(), "/api/auth/change-password", methods=["PUT"])
app.add_route(StudentProfileView.as_view(), "/api/students/me", methods=["GET"])
app.add_route(UpdateProfileView.as_view(), "/api/students/me", methods=["PUT"])
app.add_route(GradeQueryView.as_view(), "/api/grades", methods=["GET"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
