import os
from typing import List, Dict
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Configs(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI")
    
    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    DB: str = os.getenv("DB", "postgresql")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    ENV_DATABASE_MAPPER: Dict[str, str] = {
        "development": os.getenv("DB_NAME", "FastAPI"),
        "stage": f"{os.getenv('DB_NAME', 'FastAPI')}-stage",
        "testing": f"{os.getenv('DB_NAME', 'FastAPI')}-test",
        "production": os.getenv("DB_NAME", "FastAPI"),
    }
    DB_ENGINE_MAPPER: Dict[str, str] = {
        "postgresql": "postgresql+psycopg2",
        "mysql": "mysql+pymysql",
    }
    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "postgresql+psycopg2")
    DB_URI: str = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{ENV_DATABASE_MAPPER.get(ENV)}"

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret")
    JWT_ACCESS_TOKEN_EXP: str = os.getenv("ACCESS_TOKEN_EXP", "1d")
    JWT_REFRESH_TOKEN_EXP: str = os.getenv("REFRESH_TOKEN_EXP", "7d")

    CORS_ORIGINS: List[str] = os.getenv("CORS_ALLOWED_HOSTS", "*").split(",")

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"

    class Config:
        case_sensitive = True

class TestConfigs(Configs):
    ENV: str = "testing"

configs = Configs()

if configs.ENV == "production":
    pass
elif configs.ENV == "development":
    pass
elif configs.ENV == "stage":
    pass
elif configs.ENV == "testing":
    configs = TestConfigs()
