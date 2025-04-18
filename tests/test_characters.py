import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
# TODO: this may need cleanup

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

@pytest.mark.asyncio
async def test_list_characters():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create a character first to ensure empty list is not returned
        await ac.post("/characters/", json={
            "name": "Ezio",
            "level": 10,
            "class_type": "Archer"
        })
        response = await ac.get("/characters/")
        assert response.status_code == 200
        characters = response.json()
        assert isinstance(characters, list)
        assert len(characters) > 0
        assert "name" in characters[0]
        assert "level" in characters[0]
        assert "class_type" in characters[0]
        assert "id" in characters[0]
        assert "created_at" in characters[0]

@pytest.mark.asyncio
async def test_get_character():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # one again, create a character first
        char_payload = {
            "name": "Geralt",
            "level": 20,
            "class_type": "Mage"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]

        response = await ac.get(f"/characters/{char_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Geralt"
        assert response.json()["level"] == 20
        assert response.json()["class_type"] == "Mage"

@pytest.mark.asyncio
async def test_update_character():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create a character first
        char_payload = {
            "name": "Link",
            "level": 5,
            "class_type": "Ranger"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]
        # update the character
        update_payload = {
            "name": "Link",
            "level": 10,
            "class_type": "Rogue"
        }
        response = await ac.put(f"/characters/{char_id}", json=update_payload)
        assert response.status_code == 200
        assert response.json()["level"] == 10
        assert response.json()["class_type"] == "Rogue"

@pytest.mark.asyncio
async def test_delete_character():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create a character first
        char_payload = {
            "name": "Cloud",
            "level": 30,
            "class_type": "Warrior"
        }
        char_response = await ac.post("/characters/", json=char_payload)
        char_id = char_response.json()["id"]

        response = await ac.delete(f"/characters/{char_id}")
        assert response.status_code == 204

        # try to get the deleted character
        response = await ac.get(f"/characters/{char_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Character not found"