import httpx
import pytest
from app.main import app


@pytest.fixture
async def access_token():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/access-token", data={"username": "johndoe@example.com", "password": "secret"})
        assert response.status_code == 200
        return response.json()["access_token"]


@pytest.mark.asyncio
async def test_get_user(access_token):
    token = await access_token
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["email"] == "johndoe@example.com"
        assert response.json()["id"] == 1


@pytest.mark.asyncio
async def test_get_user_by_id(access_token):
    token = await access_token
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/user/1", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["email"] == "johndoe@example.com"
