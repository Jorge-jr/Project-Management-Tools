import httpx
import pytest
from app.main import app


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


@pytest.mark.asyncio
async def test_login_with_nonexistent_user():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("auth/access-token", data={"username": "nonexistent@example.com", "password": "bad_password"})
    assert response.status_code == 400, response.json()
    assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.asyncio
async def test_get_user_by_id(get_test_user):
    user_response = await get_test_user
    test_user_id = user_response.json()["id"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/user/{test_user_id}")
        assert response.status_code == 200, user_response.json().keys()
        assert response.json()["email"] == "test_user@example.com", user_response


@pytest.mark.asyncio
async def test_get_user_by_id_failure():
    test_user_id = -1
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/user/{test_user_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "user not found"


@pytest.mark.asyncio
async def test_delete_current_user(access_token):
    token_response = await access_token
    token = token_response["access_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete(
            "/user/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204
        user_response = await ac.get(f"/user/me", headers={"Authorization": f"Bearer {token}"})
        assert user_response.json()["is_deleted"] is True, user_response


@pytest.mark.asyncio
async def test_undo_delete_user_by_id(get_test_user):
    user_response = await get_test_user
    test_user_id = user_response.json()["id"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        delete_response = await ac.post(f"/user/undo_delete/?user_id={test_user_id}")
        assert delete_response.status_code == 200, delete_response
        get_user_response = await ac.get(f"/user/{test_user_id}")
        assert get_user_response.json()["is_deleted"] is False, get_user_response.json()["is_deleted"]


@pytest.mark.asyncio
async def test_delete_user_by_id(get_test_user):
    test_user_response = await get_test_user
    user_id = test_user_response["id"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete(
            f"/user/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204
        user_response = await ac.get(f"/user/me", headers={"Authorization": f"Bearer {token}"})
        assert user_response.json()["is_deleted"] is True, user_response


@pytest.mark.asyncio
async def test_register_existing_email():
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
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot use this email address"}


@pytest.mark.asyncio
async def test_get_current_user_work_items(access_token):
    token_response = await access_token
    token = token_response["access_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("user/me/work_items", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.json()["detail"]
    assert "items" in response.json()


@pytest.mark.asyncio
async def test_delete_user_by_id(access_token):
    token_response = await access_token
    token = token_response["access_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        user_response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
        user_id = user_response.json()["id"]
        delete_response = await ac.delete(f"/user/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_users():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/user/all")
    assert response.status_code == 200, response.json()
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_register_new_user():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/user/register",
            json={
                "email": "new_user@example.com",
                "password": "secret",
                "name": "new_user",
                "role": 0
            }
        )
    assert response.status_code == 200
    assert response.json()["email"] == "new_user@example.com"


# TODO: register with invalid email
