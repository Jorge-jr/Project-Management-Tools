import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


environment = os.getenv("ENVIRONMENT", "development")
dotenv_file = f".env.{environment.lower()}"
print(f"loading config from {dotenv_file}")
load_dotenv(dotenv_file)


class Settings(BaseSettings):
    environment: str = "testing"
    testing: bool = False
    secret_key: str = ""  # openssl rand -hex 32
    algorithm: str = "HS256"
    jwt_expire_minutes: int = 6
    database_url: Optional[str] = "postgresql+asyncpg://postgres:postgres@localhost/TEST_PMT"

    class Config:
        env_file = ".env"


settings = Settings()
