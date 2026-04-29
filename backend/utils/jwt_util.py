import datetime

import jwt

from config import Config


class JWTUtil:
    SECRET = Config.JWT_SECRET
    EXPIRES = Config.JWT_EXPIRES

    @classmethod
    def generate_token(cls, payload):
        token_payload = dict(payload)
        token_payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=cls.EXPIRES)
        return jwt.encode(token_payload, cls.SECRET, algorithm="HS256")

    @classmethod
    def verify_token(cls, token):
        try:
            payload = jwt.decode(token, cls.SECRET, algorithms=["HS256"])
            return payload, None
        except jwt.ExpiredSignatureError:
            return None, "Token已过期"
        except jwt.InvalidTokenError:
            return None, "Token无效"
