from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterOut
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=CharacterOut, status_code=201)
def create_character(char: CharacterCreate, db: Session = Depends(get_db)):
    db_char = Character(**char.model_dump())
    db.add(db_char)
    db.commit()
    db.refresh(db_char)
    return db_char

@router.get("/", response_model=List[CharacterOut])
def list_characters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Character).offset(skip).limit(limit).all()

@router.get("/{char_id}", response_model=CharacterOut)
def get_character(char_id: int, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return char
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

