import httpx
import pytest
from app.main import app


@pytest.mark.asyncio
async def test_access_token():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response1 = await ac.post("/auth/access-token", data={"username": "johndoe@example.com", "password": "secret"})
        response2 = await ac.post("/auth/access-token",
                                 data={"username": "invaliduser@example.com", "password": "wrongpassword"})
    assert response1.status_code == 200
    assert "access_token" in response1.json()
    assert response2.status_code == 400
    assert "detail" in response2.json()

