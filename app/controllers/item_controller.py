from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.items import Item
from app.schemas.item import ItemCreate, ItemOut
from typing import List, Optional
from app.exceptions.http_exceptions import NotFoundException, ConflictException
from sqlalchemy import and_

def create_item_controller(item: ItemCreate, db: Session = Depends(get_db)):
    # check for *exact* match across name, slot, and power
    existing = db.query(Item).filter(
        and_(
            Item.name == item.name,
            Item.slot == item.slot,
            Item.power == item.power
        )
    ).first()
    if existing:
        return existing
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list_items_controller(skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Item).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def get_item_controller(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise NotFoundException("Item not found")
    return item


def delete_item_controller(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise NotFoundException("Item not found")
    db.delete(item)
    db.commit()
    return None

def update_item_controller(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise NotFoundException("Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item_controller(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise NotFoundException("Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item



