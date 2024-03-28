import pytest
from app.main import app
import asyncio
import httpx


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

