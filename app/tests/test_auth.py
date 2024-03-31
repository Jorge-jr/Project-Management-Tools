import time
import pytest
from app.main import app
import httpx
from app.core.config import settings


@pytest.fixture
async def create_test_user():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
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
async def delete_test_user(access_token):
    token = await access_token
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        await ac.delete("user/me", headers={"Authorization": f"Bearer {token}"})


@pytest.fixture
async def refresh_token(access_token):
    await access_token
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/access-token", data={"username": "test_user@example.com", "password": "secret"})
        return response.json()["refresh_token"]


@pytest.mark.asyncio
async def test_get_access_token(access_token):
    await access_token
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/access-token", data={"username": "test_user@example.com", "password": "secret"})
    assert response.status_code == 200, response.json()["detail"]
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_access_token_failure():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/access-token",
            data={"username": "invaliduser@example.com", "password": "wrong_password"
                  }
        )
    assert response.status_code == 400
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_token_expired(access_token):
    access_token = await access_token
    token = access_token["access_token"]
    time.sleep(settings.jwt_expire_minutes + 1)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403, f"{response.status_code} - {response.json()['detail']}"
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_token_not_expired(access_token):
    access_token = await access_token
    token = access_token["access_token"]
    time.sleep(settings.jwt_expire_minutes // 2)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"error: {response.json()['detail']}"


@pytest.mark.asyncio
async def test_refresh_token(refresh_token):
    token = await refresh_token

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("auth/refresh-token", json={"refresh_token": token})

    assert response.status_code == 200, f"error: {response.json()['detail']} token: {token}"
    assert "access_token" in response.json()
