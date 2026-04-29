import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
    DB_NAME = os.getenv("DB_NAME", "grade_system")
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 10))

    JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_EXPIRES = int(os.getenv("JWT_EXPIRES", 86400))

    GPA_RULES = [
        (90, 4.0),
        (85, 3.7),
        (82, 3.3),
        (78, 3.0),
        (75, 2.7),
        (72, 2.3),
        (68, 2.0),
        (64, 1.5),
        (60, 1.0),
        (0, 0.0),
    ]
