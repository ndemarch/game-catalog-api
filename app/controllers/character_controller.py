from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterOut
from app.utils.abilities import DEFAULT_ABILITIES
from app.exceptions.http_exceptions import NotFoundException


def create_character_controller(char: CharacterCreate, db: Session = Depends(get_db)):
    abilities = DEFAULT_ABILITIES[char.class_type.value]
    db_char = Character(**char.model_dump(), abilities=abilities)
    db.add(db_char)
    db.commit()
    db.refresh(db_char)
    return db_char

def list_characters_controller(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Character).offset(skip).limit(limit).all()

def get_character_controller(char_id: int, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        raise NotFoundException("Character not found")
    return char

def delete_character_controller(char_id: int, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        raise NotFoundException("Character not found")
    db.delete(char)
    db.commit()
    return None

def update_character_controller(char_id: int, char: CharacterCreate, db: Session = Depends(get_db)):
    db_char = db.query(Character).filter(Character.id == char_id).first()
    if not db_char:
        raise NotFoundException("Character not found")
    for key, value in char.model_dump().items():
        setattr(db_char, key, value)
    db.commit()
    db.refresh(db_char)
    return db_char