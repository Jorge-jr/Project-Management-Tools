import time
import pytest
from app.main import app
import httpx
from app.core.config import settings


@pytest.fixture
async def access_token():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/access-token", data={"username": "johndoe@example.com", "password": "secret"})
        assert response.status_code == 200
        return response.json()["access_token"]


@pytest.mark.asyncio
async def test_access_token_success():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/access-token", data={"username": "johndoe@example.com", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_access_token_failure():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/access-token", data={"username": "invaliduser@example.com", "password": "wrongpassword"})
    assert response.status_code == 400
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_token_expired(access_token):
    token = await access_token
    time.sleep(settings.jwt_expire_minutes + 1)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403, f"{response.status_code} - {response.json()['detail']}"
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_token_not_expired(access_token):
    token = await access_token
    time.sleep(settings.jwt_expire_minutes // 2)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"what?{response.json()['detail']}"
