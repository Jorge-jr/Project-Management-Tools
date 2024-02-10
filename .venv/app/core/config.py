from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"
    testing: bool = False
    secret_key: str = "240632834bd534936847fe950d86a15ccbcaf08f7175c7b4e53b43979d28e37e"  # openssl rand -hex 32
    algorithm: str = "HS256"
    jwt_expire_minutes: int = 11520
    jwt_refresh_token_expire_minutes: int = 40320
    # Database URL for production
    database_url: Optional[str] = "postgresql+asyncpg://postgres:postgres@localhost/PMT"

    test_sqlalchemy_database_uri: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()