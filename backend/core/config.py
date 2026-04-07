from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "PixelDex Pro"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pixeldex"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    POKEAPI_BASE_URL: str = "https://pokeapi.co/api/v2"
    POKEAPI_REQUEST_TIMEOUT: int = 30
    POKEAPI_BATCH_SIZE: int = 50

    COBBLEMON_SHEET_URL: str = ""
    COBBLEMON_SHEET_ID: str = ""
    COBBLEMON_SERVICE_ACCOUNT_FILE: str = ""

    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
