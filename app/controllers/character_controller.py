from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterOut
from app.utils.abilities import DEFAULT_ABILITIES
from app.exceptions.http_exceptions import NotFoundException


async def create_character_controller(
    char: CharacterCreate, db: AsyncSession = Depends(get_db)
):
    abilities = DEFAULT_ABILITIES[char.class_type.value]
    db_char = Character(**char.model_dump(), abilities=abilities)
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
