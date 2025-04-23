from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.attributes import flag_modified
from app.db import get_db
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterOut
from app.utils.abilities import DEFAULT_ABILITIES
from app.utils.loadouts import DEFAULT_LOADOUTS
from app.exceptions.http_exceptions import NotFoundException, BadRequestException


async def create_character_controller(
    char: CharacterCreate, db: AsyncSession = Depends(get_db)
):
    abilities = DEFAULT_ABILITIES[char.class_type.value]
    default_loadout = DEFAULT_LOADOUTS[char.class_type.value]
    loadout = {
        item["slot"].value: {
            "name": item["name"],
            "damage": item["damage"],
            "durability": item["durability"],
            "defense": item["defense"],
        }
        for item in default_loadout
    }
    db_char = Character(
        **char.model_dump(), 
        abilities=abilities, 
        loadout=loadout 
    )
    db.add(db_char)
    await db.commit()
    await db.refresh(db_char)
    return db_char



async def list_characters_controller(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Character).offset(skip).limit(limit))
    return result.scalars().all()


async def get_character_controller(
    char_id: int, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Character).filter(Character.id == char_id))
    char = result.scalar_one_or_none()
    if not char:
        raise NotFoundException("Character not found")
    return char


async def delete_character_controller(
    char_id: int, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Character).filter(Character.id == char_id))
    char = result.scalar_one_or_none()
    if not char:
        raise NotFoundException("Character not found")
    await db.delete(char)
    await db.commit()
    return None


async def update_character_controller(
    char_id: int, char: CharacterCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Character).filter(Character.id == char_id))
    db_char = result.scalar_one_or_none()
    if not db_char:
        raise NotFoundException("Character not found")
    for key, value in char.model_dump().items():
        setattr(db_char, key, value)
    await db.commit()
    await db.refresh(db_char)
    return db_char


async def update_character_item_controller(
    character_id: int,
    payload: dict,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalars().first()
    if not character:
        raise NotFoundException("Character not found")
    slot = payload.get("slot")
    item = payload.get("item")
    if not slot or not item:
        raise BadRequestException("Slot and item must be provided in the payload")
    loadout = character.loadout or {}
    loadout[slot] = item
    character.loadout = loadout
    flag_modified(character, "loadout") # because we only update part of the dict
    db.add(character)
    await db.commit()
    await db.refresh(character)
    return character