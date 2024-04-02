import time
import pytest
import asyncio
import httpx
from app.core.config import settings
from app.main import app


@pytest.mark.asyncio(scope="session")
async def test_get_access_token(create_test_user_gen):
    user_gen = create_test_user_gen
    user = await anext(user_gen)
    email = user["email"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/access-token", data={"username": email, "password": "password"})
    assert response.status_code == 200, response.json()["detail"]
    assert "access_token" in response.json()
    await anext(user_gen)


@pytest.mark.asyncio(scope="session")
async def test_access_token_failure():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/access-token",
            data={"username": "invaliduser@example.com", "password": "wrong_password"
                  }
        )
    assert response.status_code == 400
    assert "detail" in response.json()


@pytest.mark.asyncio(scope="session")
async def test_token_expired(get_test_user_token_gen):
    token_gen = get_test_user_token_gen
    token_response = await anext(token_gen)
    token = token_response["access_token"]
    await asyncio.sleep(settings.jwt_expire_minutes + 1)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403, f"{response.status_code} - {response.json()['detail']}"
    assert "detail" in response.json()
    await anext(token_gen)


@pytest.mark.asyncio(scope="session")
async def test_token_not_expired(get_test_user_token_gen):
    token_gen = get_test_user_token_gen
    token_response = await anext(token_gen)
    token = token_response["access_token"]
    await asyncio.sleep(settings.jwt_expire_minutes // 2)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"error: {response.json()['detail']}"
    await anext(token_gen)


@pytest.mark.asyncio(scope="session")
async def test_refresh_token(get_test_user_token_gen):
    token_gen = get_test_user_token_gen
    token_response = await anext(token_gen)
    token = token_response["refresh_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("auth/refresh-token", json={"refresh_token": token})

    assert response.status_code == 200, f"error: {response.json()['detail']} token: {token}"
    assert "access_token" in response.json()
    await anext(token_gen)
