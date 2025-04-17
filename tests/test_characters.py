import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_character():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "name": "Aloy",
            "level": 15,
            "class_type": "Warrior"
        }
        response = await ac.post("/characters/", json=payload)
        assert response.status_code == 201
        assert response.json()["name"] == "Aloy"
