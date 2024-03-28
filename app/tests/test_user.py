import httpx
import pytest
from app.main import app


@pytest.mark.asyncio
async def test_access_token():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/access-token", data={"username": "johndoe@example.com", "password": "secret"})
        print(response)