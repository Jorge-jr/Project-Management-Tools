import asyncio
import pytest
import httpx
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def create_test_user():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/user/register",
            json={
                "email": "test_user@example.com",
                "password": "secret",
                "name": "test_user",
                "role": 0
            }
        )


@pytest.fixture
async def access_token(create_test_user):
    await create_test_user
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        login_response = await ac.post(
            "/auth/access-token",
            data={
                "username": "test_user@example.com",
                "password": "secret"
            }
        )
        return login_response.json()


@pytest.fixture
async def get_test_user(access_token):
    token_response = await access_token
    token = token_response["access_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        login_response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
        return login_response
