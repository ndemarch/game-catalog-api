import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_loadout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # First, create a character
        char_payload = {
            "name": "Jinx",
            "level": 7,
            "class_type": "Rogue"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]

        # Create a loadout for that character
        loadout_payload = {
            "item_name": "Crossbow",
            "slot": "Weapon",
            "power": 40,
            "character_id": char_id
        }

        loadout_response = await ac.post("/loadouts/", json=loadout_payload)
        assert loadout_response.status_code == 201
        assert loadout_response.json()["item_name"] == "Crossbow"
        assert loadout_response.json()["slot"] == "Weapon"
        assert loadout_response.json()["power"] == 40
        assert loadout_response.json()["character_id"] == char_id
