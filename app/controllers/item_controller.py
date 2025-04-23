from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models.items import Item
from app.schemas.item import ItemCreate, ItemOut
from typing import List, Optional
from app.exceptions.http_exceptions import NotFoundException, ConflictException
from sqlalchemy import and_
from sqlalchemy.future import select

async def create_item_controller(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    # avoiding duplicates but this may not be necessary
    query = select(Item).filter(
        and_(
            Item.name == item.name,
            Item.slot == item.slot,
            Item.damage == item.damage,
            Item.defense == item.defense,
            Item.durability == item.durability,
            Item.weight == item.weight,
            Item.rarity == item.rarity,
        )
    )
    result = await db.execute(query)
    existing = result.scalars().first()
    if existing:
        return existing
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def list_items_controller(skip: int = 0, limit: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Item).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_item_controller(item_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Item).filter(Item.id == item_id)
    result = await db.execute(query)
    item = result.scalars().first()
    if not item:
        raise NotFoundException("Item not found")
    return item


async def delete_item_controller(item_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Item).filter(Item.id == item_id)
    result = await db.execute(query)
    item = result.scalars().first()
    if not item:
        raise NotFoundException("Item not found")
    await db.delete(item)
    await db.commit()
    return None


async def update_item_controller(item_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db)):
    query = select(Item).filter(Item.id == item_id)
    result = await db.execute(query)
    db_item = result.scalars().first()
    if not db_item:
        raise NotFoundException("Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item
