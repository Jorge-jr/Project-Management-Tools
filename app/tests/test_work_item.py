import httpx
import pytest
from app.main import app


@pytest.mark.asyncio
async def test_get_work_items(access_token):
    token_response = await access_token
    token = token_response["access_token"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/work_item/work_item_list", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert isinstance(response.json(), list), response.json()


@pytest.mark.asyncio
async def test_create_work_item(create_test_user_gen):

    user_generator = create_test_user_gen
    user = await anext(user_generator)  # create user

    assert user is not None, user

    delete_user_response = await anext(user_generator)  # delete user

    assert delete_user_response is None, delete_user_response


'''
@pytest.mark.asyncio
async def test_create_work_item(get_test_user_gen):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/work_item/create", json={
            "title": "Test Work Item",
            "description": "This is a test work item",
            "due_date": "2023-04-01T00:00:00",
            "initial_date": "2023-03-01T00:00:00",
            "status": "NEW",
            "work_item_type": "TASK",
            "driver_id": 1 # Assuming a user with ID 1 exists
        })
        assert response.status_code == 201
        assert "id" in response.json()


@pytest.mark.asyncio
async def test_update_work_item():
    # Assuming a work item with ID 1 exists
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put("/work_item/update/1", json={
            "title": "Updated Work Item",
            "description": "This is an updated work item",
            "due_date": "2023-04-02T00:00:00",
            "status": "IN_PROGRESS",
            "work_item_type": "TASK"
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Work Item"


@pytest.mark.asyncio
async def test_delete_work_item():
    # Assuming a work item with ID 1 exists
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete("/work_item/delete/1")
        assert response.status_code == 204


@pytest.mark.asyncio
async def test_soft_delete_work_item():
    # Assuming a work item with ID 1 exists
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/work_item/soft_delete/1")
        assert response.status_code == 200
        assert response.json()["is_deleted"] is True


@pytest.mark.asyncio
async def test_restore_work_item():
    # Assuming a work item with ID 1 exists and has been soft deleted
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/work_item/restore/1")
        assert response.status_code == 200
        assert response.json()["is_deleted"] is False
'''