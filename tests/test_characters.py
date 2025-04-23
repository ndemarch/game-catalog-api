from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import AsyncClient, ASGITransport
from app.main import app
import pytest

@pytest.mark.asyncio
async def test_create_character(client):
    payload = {
        "name": "Aloy",
        "level": 15,
        "class_type": "Warrior"
    }
    response = await client.post("/characters/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Aloy"
    assert data["level"] == 15
    assert data["class_type"] == "Warrior"

@pytest.mark.asyncio
async def test_list_characters(client):
    # ensure there's at least one character
    await client.post("/characters/", json={
        "name": "Ezio",
        "level": 10,
        "class_type": "Archer"
    })

    response = await client.get("/characters/")
    assert response.status_code == 200
    characters = response.json()

    assert isinstance(characters, list)
    assert len(characters) > 0

    keys = {"id", "name", "level", "class_type", "created_at"}
    assert keys.issubset(characters[0].keys())

@pytest.mark.asyncio
async def test_get_character(client):
    create_payload = {
        "name": "Geralt",
        "level": 20,
        "class_type": "Mage"
    }
    create_response = await client.post("/characters/", json=create_payload)
    char_id = create_response.json()["id"]

    response = await client.get(f"/characters/{char_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Geralt"
    assert data["level"] == 20
    assert data["class_type"] == "Mage"

@pytest.mark.asyncio
async def test_update_character(client):
    # ensure one character exists
    create_payload = {
        "name": "Link",
        "level": 5,
        "class_type": "Ranger"
    }
    create_response = await client.post("/characters/", json=create_payload)
    char_id = create_response.json()["id"]
    # update
    update_payload = {
        "name": "Link",
        "level": 10,
        "class_type": "Rogue"
    }
    response = await client.put(f"/characters/{char_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == 10
    assert data["class_type"] == "Rogue"
    assert data["updated_at"] is not None

@pytest.mark.asyncio
async def test_delete_character(client):
    # ensure one character exists
    create_payload = {
        "name": "Cloud",
        "level": 30,
        "class_type": "Warrior"
    }
    create_response = await client.post("/characters/", json=create_payload)
    char_id = create_response.json()["id"]
    # delete
    response = await client.delete(f"/characters/{char_id}")
    assert response.status_code == 204
    # ensure deletion
    response = await client.get(f"/characters/{char_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_character_loadout(client):
    # ensure one character exists
    create_payload = {
        "name": "Cloud",
        "level": 30,
        "class_type": "Warrior"
    }
    first_response = await client.post("/characters/", json=create_payload)
    char_id = first_response.json()["id"]
    # define the payload to update the loadout
    payload = {
        "slot": "Weapon",
        "item": {
            "name": "Great Sword",
            "damage": 15.0,
            "durability": 100.0,
            "defense": 0.0
        }
    }
    # update the loadout
    second_response = await client.patch(f"/characters/{char_id}/loadout", json=payload)
    assert second_response.status_code == 200
    # get the character to verify the loadout
    final_response = await client.get(f"/characters/{char_id}")
    assert final_response.status_code == 200
    character_data = final_response.json()
    # validate the loadout update
    assert character_data["loadout"]["Weapon"] == {
        "name": "Great Sword",
        "damage": 15.0,
        "durability": 100.0,
        "defense": 0.0
    }