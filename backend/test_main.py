from main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

client = TestClient(app)


@pytest.mark.anyio
async def test_read_main():
    async with AsyncClient(app=app, base_url="https://dev.himaaa.xyz/") as ac:
        response = await ac.get("/user")

        print(response.json)
    assert response.status_code == 307


