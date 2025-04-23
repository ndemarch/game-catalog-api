import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
# TODO: may need some cleanup

@pytest.mark.asyncio
async def test_create_item(client):
    item_payload = {
        "name": "Crossbow",
        "slot": "Weapon",
        "damage": 40.0,
        "durability": 100.0,
        "defense": 0.0,
        "weight": 2.5,
        "rarity": "Rare",
    }
    response = await client.post("/items/", json=item_payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Crossbow"
    assert response.json()["slot"] == "Weapon"
    assert response.json()["damage"] == 40.0
    assert response.json()["durability"] == 100.0
    assert response.json()["defense"] == 0.0
    assert response.json()["weight"] == 2.5
    assert response.json()["rarity"] == "Rare"

@pytest.mark.asyncio
async def test_list_items(client):
    # ensure there's at least one item
    item_payload = {
        "name": "Pulse Pistol",
        "slot": "Weapon",
        "damage": 30.0,
        "durability": 100.0,
        "defense": 0.0,
        "weight": 1.5,
        "rarity": "Common",
    }
    await client.post("/items/", json=item_payload)
    # get the list of items or item
    response = await client.get("/items/")
    assert response.status_code == 200
    loadouts = response.json()
    assert isinstance(loadouts, list)
    assert len(loadouts) > 0
    assert "name" in loadouts[0]
    assert "slot" in loadouts[0]
    assert "damage" in loadouts[0]
    assert "durability" in loadouts[0]
    assert "defense" in loadouts[0]
    assert "weight" in loadouts[0]
    assert "rarity" in loadouts[0]


@pytest.mark.asyncio
async def test_get_item(client):
    # ensure one item exists
    item_payload = {
        "name": "Rocket Hammer",
        "slot": "Weapon",
        "damage": 50.0,
        "durability": 100.0,
        "defense": 0.0,
        "weight": 3.0,
        "rarity": "Epic",
    }
    loadout_response = await client.post("/items/", json=item_payload)
    item_id = loadout_response.json()["id"]
    # get the item
    response = await client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Rocket Hammer"
    assert response.json()["slot"] == "Weapon"
    assert response.json()["damage"] == 50.0
    assert response.json()["durability"] == 100.0
    assert response.json()["defense"] == 0.0
    assert response.json()["weight"] == 3.0
    assert response.json()["rarity"] == "Epic"

@pytest.mark.asyncio
async def test_update_item(client):
    # ensure one item exists
    item_payload = {
        "name": "Power Gauntlet",
        "slot": "Weapon",
        "damage": 60.0,
        "durability": 100.0,
        "defense": 0.0,
        "weight": 1.0,
        "rarity": "Legendary",
    }
    response = await client.post("/items/", json=item_payload)
    item_id = response.json()["id"]
    # update the item
    update_payload = {
        "name": "Power Gauntlet",
        "slot": "Weapon",
        "damage": 70.0,
        "durability": 100.0,
        "defense": 0.0,
        "weight": 1.0,
        "rarity": "Legendary",
    }
    new_response = await client.put(f"/items/{item_id}", json=update_payload)
    assert new_response.status_code == 200
    assert new_response.json()["damage"] == 70.0

@pytest.mark.asyncio
async def test_delete_item(client):
    item_payload = {
        "name": "Power Gauntlet",
        "slot": "Weapon",
        "damage": 60.0,
        "durability": 100.0,
        "defense": 0.0,
        "weight": 1.0,
        "rarity": "Legendary",
    }
    response = await client.post("/items/", json=item_payload)
    item_id = response.json()["id"]
    # delete the item
    new_response = await client.delete(f"/items/{item_id}")
    assert new_response.status_code == 204
