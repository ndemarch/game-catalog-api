from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterOut
from typing import List, Optional
from app.controllers.character_controller import (
    create_character_controller,
    list_characters_controller,
    get_character_controller,
    delete_character_controller,
    update_character_controller
)

# character api router: handles character-related endpoints
# I mount this router in main.py for the app
router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)

@router.post("/", response_model=CharacterOut, status_code=201)
def create_character(char: CharacterCreate, db: Session = Depends(get_db)):
    return create_character_controller(char, db)

@router.get("/{char_id}", response_model=CharacterOut)
def get_character(char_id: int, db: Session = Depends(get_db)):
    return get_character_controller(char_id, db)

@router.delete("/{char_id}", status_code=204)
def delete_character(char_id: int, db: Session = Depends(get_db)):
    return delete_character_controller(char_id, db)

@router.put("/{char_id}", response_model=CharacterOut)
def update_character(char_id: int, char: CharacterCreate, db: Session = Depends(get_db)):
    return update_character_controller(char_id, char, db)

@router.get("/", response_model=List[CharacterOut])
def list_characters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_characters_controller(skip, limit, db)


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

