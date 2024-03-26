import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    environment: str = "development"
    testing: bool = False
    secret_key: str = ""
    algorithm: str = "HS256"
    jwt_expire_minutes: int = 11520
    jwt_refresh_token_expire_minutes: int = 40320
    database_url: Optional[str] = None
    test_database_url: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()

print(settings)

