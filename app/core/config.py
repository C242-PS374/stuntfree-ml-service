import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

ENV: str = ""

class Configs(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI")
    ENV_DATABASE_MAPPER: dict = {
        "development": os.getenv("DB_NAME", "FastAPI"),
        "stage": os.getenv("DB_NAME", "FastAPI") + "-stage",
        "testing": os.getenv("DB_NAME", "FastAPI") + "-test",
        "production": os.getenv("DB_NAME", "FastAPI"),
    }
    DB_ENGINE_MAPPER : dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
    }

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # Database
    DB: str = os.getenv("DB", "postgresql")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_ENGINE: str = DB_ENGINE_MAPPER[DB]

    DB_URI: str = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{ENV_DATABASE_MAPPER[ENV]}"

    # Auth
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret")
    JWT_ACCESS_TOKEN_EXP: str = os.getenv("ACCESS_TOKEN_EXP", "1d")
    JWT_REFRESH_TOKEN_EXP: str = os.getenv("REFRESH_TOKEN_EXP", "7d")  

    # Cors
    CORS_ORIGINS: List[str] = os.getenv("CORS_ALLOWED_HOSTS", "*").split(",")

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"
    
    class Config:
        case_sensitive = True

class TestConfigs(Configs):
    ENV: str = "test"

configs = Configs()

if ENV == "production":
    pass
elif ENV == "development":
    pass
elif ENV == "stage":
    pass
elif ENV == "testing":
    setting = TestConfigs()