import httpx
import pytest
from app.main import app


@pytest.mark.asyncio
async def test_login_with_nonexistent_user():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("auth/access-token", data={"username": "nonexistent@example.com", "password": "bad_password"})
    assert response.status_code == 400, response.json()
    assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.asyncio
async def test_get_user_by_id(create_test_user_gen):
    user_gen = create_test_user_gen
    user = await anext(user_gen)
    test_user_id = user["id"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/user/{test_user_id}")
        assert response.status_code == 200, user
        assert "@random.com" in response.json()["email"], user
    await anext(user_gen)


@pytest.mark.asyncio
async def test_get_user_by_id_failure():
    test_user_id = -1
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/user/{test_user_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "user not found"


@pytest.mark.asyncio
async def test_delete_current_user(get_test_user_token_gen):
    user_token_gen = get_test_user_token_gen
    token_response = await anext(user_token_gen)
    token = token_response["access_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete(
            "/user/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204
        user_response = await ac.get(f"/user/me", headers={"Authorization": f"Bearer {token}"})
        assert user_response.json()["is_deleted"] is True, user_response
    await anext(user_token_gen)


@pytest.mark.asyncio
async def test_undo_delete_user_by_id(create_test_user_gen):
    user_gen = create_test_user_gen
    user = await anext(user_gen)
    test_user_id = user["id"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        delete_response = await ac.post(f"/user/undo_delete/?user_id={test_user_id}")
        assert delete_response.status_code == 200, delete_response
        get_user_response = await ac.get(f"/user/{test_user_id}")
        assert get_user_response.json()["is_deleted"] is False, get_user_response.json()["is_deleted"]
    await anext(user_gen)


@pytest.mark.asyncio
async def test_delete_user_by_id(create_test_user_gen, get_test_admin_token_gen):
    user_gen = create_test_user_gen
    user = await anext(user_gen)
    test_user_id = user["id"]
    admin_token_gen = get_test_admin_token_gen
    admin_token = await anext(admin_token_gen)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete(
            f"/user/{test_user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 204
        user_response = await ac.get(f"/user/{test_user_id}")
        assert user_response.json()["is_deleted"] is True, user_response
    await anext(user_gen)
    await anext(admin_token_gen)


@pytest.mark.asyncio
async def test_register_existing_email(create_test_user_gen):
    user_gen = create_test_user_gen
    user = await anext(user_gen)
    email = user["email"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/user/register",
            json={
                f"email": email,
                "password": "secret",
                "name": "test_user",
                "role": 0
            }
        )
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot use this email address"}
    await anext(user_gen)


@pytest.mark.asyncio
async def test_get_current_user_work_items(get_test_user_token_gen):
    token_gen = get_test_user_token_gen
    token_response = await anext(token_gen)
    token = token_response["access_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("user/me/work_items", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.json()["detail"]
    assert "items" in response.json()
    await anext(token_gen)


@pytest.mark.asyncio
async def test_delete_user_by_id(get_test_admin_token_gen):
    admin_token_gen = get_test_admin_token_gen
    token_response = await anext(admin_token_gen)
    token = token_response["access_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        user_response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
        user_id = user_response.json()["id"]
        delete_response = await ac.delete(f"/user/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == 200
    await anext(admin_token_gen)


@pytest.mark.asyncio
async def test_get_all_users():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/user/all")
    assert response.status_code == 200, response.json()
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_register_new_user(get_test_admin_token_gen):
    admin_token_gen = get_test_admin_token_gen
    token_response = await anext(admin_token_gen)
    token = token_response["access_token"]
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
        delete_response = await ac.post(
            f"/user/hard_delete?user_id={response.json()['id']}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert delete_response.status_code == 200, delete_response.json()
        await anext(admin_token_gen)


# TODO: register with invalid email
