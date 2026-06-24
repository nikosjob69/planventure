import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SECRET = "this-is-a-very-long-and-secure-secret-key-for-planventure-api"


def _get_secret(name, fallback, min_length=32):
    value = os.getenv(name)
    if value and len(value.encode("utf-8")) >= min_length:
        return value
    return fallback


class Config:
    SECRET_KEY = _get_secret("SECRET_KEY", DEFAULT_SECRET)
    JWT_SECRET_KEY = _get_secret("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///planventure.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]
