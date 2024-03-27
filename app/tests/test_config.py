import os

from app.core.config import settings

print("Current working directory:", os.getcwd())
print("Environment variables loaded successfully.")

def test_config():
    print("Environment:", settings.environment)
    print("Testing:", settings.testing)
    print("Secret Key:", settings.secret_key)
    print("Algorithm:", settings.algorithm)
    print("JWT Expire Minutes:", settings.jwt_expire_minutes)
    print("JWT Refresh Token Expire Minutes:", settings.jwt_refresh_token_expire_minutes)
    print("Database URL:", settings.database_url)
    print("Test Database URL:", settings.test_database_url)


if __name__ == "__main__":
    test_config()
