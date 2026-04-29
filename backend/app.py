from sanic import Sanic

from api.v1.auth import LoginView
from api.v1.grade import GradeQueryView
from mappers.base_mapper import BaseMapper
from middleware.auth_middleware import auth_middleware


app = Sanic("GradeSystem")


@app.listener("before_server_stop")
async def close_database_pool(app, loop):
    await BaseMapper.close_pool()


@app.middleware("request")
async def verify_token(request):
    if request.path == "/api/auth/login":
        return None

    if request.path.startswith("/api/grades"):
        return await auth_middleware(request)

    return None


app.add_route(LoginView.as_view(), "/api/auth/login", methods=["POST"])
app.add_route(GradeQueryView.as_view(), "/api/grades", methods=["GET"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
