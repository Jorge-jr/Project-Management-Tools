import os

import pytest

from app.core.config import settings


@pytest.mark.asyncio(scope="session")
async def test_config():
    assert settings.environment.upper() == 'TESTING'
    assert settings.testing is True
    print("Secret Key:", settings.secret_key)
    print("Algorithm:", settings.algorithm)
    print("JWT Expire Minutes:", settings.jwt_expire_minutes)
    print("Database URL:", settings.database_url)


if __name__ == "__main__":
    test_config()


# TODO: refactor
