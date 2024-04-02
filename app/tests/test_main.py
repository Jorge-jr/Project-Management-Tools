import httpx
import pytest
from app.main import *


@pytest.mark.asyncio(scope='session')
async def test_read_main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
