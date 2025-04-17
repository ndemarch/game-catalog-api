from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.loadout import Loadout
from app.schemas.loadout import LoadoutCreate, LoadoutOut
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=LoadoutOut, status_code=201)
def create_loadout(loadout: LoadoutCreate, db: Session = Depends(get_db)):
    db_loadout = Loadout(**loadout.model_dump())
    db.add(db_loadout)
    db.commit()
    db.refresh(db_loadout)
    return db_loadout

@router.get("/", response_model=List[LoadoutOut])
def list_loadouts(skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Loadout).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

@router.get("/characters/{character_id}", response_model=List[LoadoutOut])
def get_loadouts_for_character(character_id: int, db: Session = Depends(get_db)):
    return db.query(Loadout).filter(Loadout.character_id == character_id).all()

##pagination
#@router.get("/", response_model=List[LoadoutOut])
#def list_loadouts(
#    skip: int = 0,
#    limit: int = 10,
#    slot: Optional[str] = None,
#    min_power: Optional[int] = None,
#    db: Session = Depends(get_db)
#):
#    query = db.query(Loadout)
#    if slot:
#        query = query.filter(Loadout.slot == slot)
#    if min_power:
#        query = query.filter(Loadout.power >= min_power)
#    return query.offset(skip).limit(limit).all()
