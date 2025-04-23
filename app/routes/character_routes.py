from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas.character import CharacterCreate, CharacterOut
from typing import List
from app.controllers.character_controller import (
    create_character_controller,
    list_characters_controller,
    get_character_controller,
    delete_character_controller,
    update_character_controller,
    update_character_item_controller,
)

# character api router: handles character-related endpoints
# I mount this router in main.py for the app
router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)

@router.post("/", response_model=CharacterOut, status_code=201)
async def create_character(char: CharacterCreate, db: AsyncSession = Depends(get_db)):
    return await create_character_controller(char, db)

@router.get("/{char_id}", response_model=CharacterOut)
async def get_character(char_id: int, db: AsyncSession = Depends(get_db)):
    return await get_character_controller(char_id, db)

@router.delete("/{char_id}", status_code=204)
async def delete_character(char_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_character_controller(char_id, db)

@router.put("/{char_id}", response_model=CharacterOut)
async def update_character(char_id: int, char: CharacterCreate, db: AsyncSession = Depends(get_db)):
    return await update_character_controller(char_id, char, db)

@router.get("/", response_model=List[CharacterOut])
async def list_characters(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await list_characters_controller(skip, limit, db)

@router.patch("/{char_id}/loadout")
async def update_loadout(char_id: int, payload: dict, db: AsyncSession = Depends(get_db)):
    return await update_character_item_controller(char_id, payload, db)

##pagination
#@router.get("/", response_model=List[CharacterOut])
#def list_characters(
#    skip: int = 0,
#    limit: int = 10,
#    class_type: Optional[str] = None,
#    min_level: Optional[int] = None,
#    db: Session = Depends(get_db)
#):
#    query = db.query(Character)
#    if class_type:
#        query = query.filter(Character.class_type == class_type)
#    if min_level:
#        query = query.filter(Character.level >= min_level)
#    return query.offset(skip).limit(limit).all()
