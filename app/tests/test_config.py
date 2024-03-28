import os

from app.core.config import settings


def test_config():
    print("Environment:", settings.environment)
    print("Testing:", settings.testing)
    print("Secret Key:", settings.secret_key)
    print("Algorithm:", settings.algorithm)
    print("JWT Expire Minutes:", settings.jwt_expire_minutes)
    print("Database URL:", settings.database_url)
    print("Test Database URL:", settings.test_database_url)


if __name__ == "__main__":
    test_config()
