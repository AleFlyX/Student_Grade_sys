import hashlib


class PasswordUtil:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password, hashed):
        return PasswordUtil.hash_password(password) == hashed
