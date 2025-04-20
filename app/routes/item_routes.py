from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.items import Item
from app.schemas.item import ItemCreate, ItemOut
from typing import List, Optional
from app.controllers.item_controller import (
    create_item_controller,
    list_items_controller,
    get_item_controller,
    delete_item_controller,
    update_item_controller
)

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@router.post("/", response_model=ItemOut, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item_controller(item, db)

@router.get("/", response_model=List[ItemOut])
def list_items(skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    return list_items_controller(skip, limit, db)

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_controller(item_id, db)

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return delete_item_controller(item_id, db)

@router.put("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return update_item_controller(item_id, item, db)


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
