import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
# TODO: may need some cleanup

@pytest.mark.asyncio
async def test_create_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        item_payload = {
            "name": "Crossbow",
            "slot": "Weapon",
            "power": 40,
        }

        response = await ac.post("/items/", json=item_payload)
        assert response.status_code == 201
        assert response.json()["name"] == "Crossbow"
        assert response.json()["slot"] == "Weapon"
        assert response.json()["power"] == 40

@pytest.mark.asyncio
async def test_list_items():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        item_payload = {
            "name": "Pulse Pistol",
            "slot": "Weapon",
            "power": 30,
        }

        # create a loadout for that character
        await ac.post("/items/", json=item_payload)

        response = await ac.get("/items/")
        assert response.status_code == 200
        loadouts = response.json()
        assert isinstance(loadouts, list)
        assert len(loadouts) > 0
        assert "name" in loadouts[0]
        assert "slot" in loadouts[0]
        assert "power" in loadouts[0]


@pytest.mark.asyncio
async def test_get_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        item_payload = {
            "name": "Rocket Hammer",
            "slot": "Weapon",
            "power": 50,
        }
        loadout_response = await ac.post("/items/", json=item_payload)
        item_id = loadout_response.json()["id"]
        # get the loadout
        response = await ac.get(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Rocket Hammer"
        assert response.json()["slot"] == "Weapon"
        assert response.json()["power"] == 50

@pytest.mark.asyncio
async def test_update_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        item_payload = {
            "name": "Power Gauntlet",
            "slot": "Weapon",
            "power": 60,
        }
        response = await ac.post("/items/", json=item_payload)
        item_id = response.json()["id"]
        # update the loadout
        update_payload = {
            "name": "Power Gauntlet",
            "slot": "Weapon",
            "power": 90,
        }
        new_response = await ac.put(f"/items/{item_id}", json=update_payload)
        assert new_response.status_code == 200
        assert new_response.json()["power"] == 90

@pytest.mark.asyncio
async def test_delete_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        item_payload = {
            "name": "Power Gauntlet",
            "slot": "Weapon",
            "power": 90,
        }
        response = await ac.post("/items/", json=item_payload)
        item_id = response.json()["id"]
        # delete the loadout
        new_response = await ac.delete(f"/items/{item_id}")
        assert new_response.status_code == 204
