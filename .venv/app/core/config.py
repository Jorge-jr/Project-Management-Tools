from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"
    testing: bool = False
    secret_key: str = "240632834bd534936847fe950d86a15ccbcaf08f7175c7b4e53b43979d28e37e"  # openssl rand -hex 32
    testing_secret_key: str = "205ba98c78940b409b000de7d2b619756e91437eb7f0d2cc32eaa5aecf39a9dd"
    production_secret_key: str = "83cac4f5f0fa028fc53433949d4b9985a557b1f8ac660a8e6dd65727db125b54"
    algorithm: str = "HS256"
    jwt_expire_minutes: int = 11520
    jwt_refresh_token_expire_minutes: int = 40320
    # Database URL for production
    database_url: Optional[str] = "postgresql+asyncpg://postgres:postgres@localhost/PMT"
    test_database_urL: Optional[str] = "postgresql+asyncpg://postgres:postgres@localhost/TEST_PMT"

    class Config:
        env_file = ".env"


settings = Settings()
