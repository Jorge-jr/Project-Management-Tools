import asyncio
import pytest
import httpx
from app.main import app
import random
import string


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def create_test_user_gen(get_test_admin_token_gen):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/user/register", json={
            "email": generate_random_email(),
            "password": "password",
            "name": "Test User",
            "role": 0
        })
        assert response.status_code == 200, response.text
        user = response.json()
        yield user
        admin_token_generator = get_test_admin_token_gen
        admin_token_response = await anext(admin_token_generator)
        admin_token = admin_token_response["access_token"]
        delete_test_user_response = await ac.post(
            f"/user/hard_delete?user_id={user['id']}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        # detail = delete_test_user_response.json()["detail"]
        await anext(admin_token_generator)
        yield delete_test_user_response.json()


@pytest.fixture
async def create_test_admin_user_gen():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/user/register", json={
            "email": generate_random_email(),
            "password": "admin",
            "name": "Test admin",
            "role": 5
        })
        assert response.status_code == 200, response.text
        admin = response.json()
        yield admin
        admin_response = await ac.post(
            "/auth/access-token",
            data={
                "username": admin["email"],
                "password": "admin"
            }
        )
        admin_token = admin_response.json()["access_token"]
        delete_response = await ac.post(
            f"/user/hard_delete?user_id={admin['id']}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        yield delete_response.json()


@pytest.fixture
async def get_test_admin_token_gen(create_test_admin_user_gen):
    admin_generator = create_test_admin_user_gen
    admin = await anext(admin_generator)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "auth/access-token",
            data={
                "username": admin["email"],
                "password": "admin"
            }
        )
    yield response.json()
    delete_admin = await anext(admin_generator)
    yield delete_admin


@pytest.fixture
async def get_test_user_token_gen(create_test_user_gen):
    user_generator = create_test_user_gen
    user = await anext(user_generator)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "auth/access-token",
            data={
                "username": user["email"],
                "password": "password"
            }
        )
    yield response.json()
    delete_user = await anext(user_generator)
    yield delete_user


def generate_random_email(length=12):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))

    return random_string + "@random.com"
