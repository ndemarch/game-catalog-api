import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
# TODO: may need some cleanup

@pytest.mark.asyncio
async def test_create_loadout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create characer
        char_payload = {
            "name": "Jinx",
            "level": 7,
            "class_type": "Rogue"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]
        # create a loadout for that character
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

@pytest.mark.asyncio
async def test_list_loadouts():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create a character first to avoid empty list error
        char_payload = {
            "name": "Tracer",
            "level": 5,
            "class_type": "Archer"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]

        # create a loadout for that character
        await ac.post("/loadouts/", json={
            "item_name": "Pulse Pistol",
            "slot": "Weapon",
            "power": 30,
            "character_id": char_id
        })

        response = await ac.get("/loadouts/")
        assert response.status_code == 200
        loadouts = response.json()
        assert isinstance(loadouts, list)
        assert len(loadouts) > 0
        assert "item_name" in loadouts[0]
        assert "slot" in loadouts[0]
        assert "power" in loadouts[0]
        assert "character_id" in loadouts[0]

@pytest.mark.asyncio
async def test_get_loadout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create a character first to avoid empty list error
        char_payload = {
            "name": "Reinhardt",
            "level": 10,
            "class_type": "Mage"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]
        # create a loadout for that character
        loadout_payload = {
            "item_name": "Rocket Hammer",
            "slot": "Weapon",
            "power": 50,
            "character_id": char_id
        }
        loadout_response = await ac.post("/loadouts/", json=loadout_payload)
        loadout_id = loadout_response.json()["id"]
        # get the loadout
        response = await ac.get(f"/loadouts/{loadout_id}")
        assert response.status_code == 200
        assert response.json()["item_name"] == "Rocket Hammer"
        assert response.json()["slot"] == "Weapon"
        assert response.json()["power"] == 50
        assert response.json()["character_id"] == char_id

@pytest.mark.asyncio
async def test_update_loadout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create a character first to avoid empty list error
        char_payload = {
            "name": "Doomfist",
            "level": 15,
            "class_type": "Healer"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]
        # create a loadout for that character
        loadout_payload = {
            "item_name": "Power Gauntlet",
            "slot": "Weapon",
            "power": 60,
            "character_id": char_id
        }
        loadout_response = await ac.post("/loadouts/", json=loadout_payload)
        loadout_id = loadout_response.json()["id"]
        # update the loadout
        update_payload = {
            "item_name": "Power Gauntlet",
            "slot": "Weapon",
            "power": 80,
            "character_id": char_id
        }
        response = await ac.put(f"/loadouts/{loadout_id}", json=update_payload)
        assert response.status_code == 200
        assert response.json()["power"] == 80

@pytest.mark.asyncio
async def test_delete_loadout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create a character first to avoid empty list error
        char_payload = {
            "name": "Winston",
            "level": 20,
            "class_type": "Ranger"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]
        # create a loadout for that character
        loadout_payload = {
            "item_name": "Flame Cannon",
            "slot": "Weapon",
            "power": 100,
            "character_id": char_id
        }
        loadout_response = await ac.post("/loadouts/", json=loadout_payload)
        loadout_id = loadout_response.json()["id"]
        # delete the loadout
        response = await ac.delete(f"/loadouts/{loadout_id}")
        assert response.status_code == 204
