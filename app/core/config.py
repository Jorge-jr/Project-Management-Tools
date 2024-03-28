import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


environment = os.getenv("ENVIRONMENT", "development")
print(environment)
dotenv_file = f".env.{environment}"
load_dotenv(dotenv_file)


class Settings(BaseSettings):
    environment: str = "development"
    testing: bool = False
    secret_key: str = ""  # openssl rand -hex 32
    algorithm: str = "HS256"
    jwt_expire_minutes: int = 11520
    database_url: Optional[str] = None
    test_database_url: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
