from sqlalchemy import Column, Integer, String, Enum, UniqueConstraint
from app.db import Base
import enum

class SlotType(str, enum.Enum):
    helmet = "Helmet"
    armour = "Armour"
    gloves = "Gloves"
    boots = "Boots"
    weapon = "Weapon"
    shield = "Shield"

class Item(Base):
    __tablename__ = "items"
    #__table_args__ = (
    #    UniqueConstraint('name', 'slot', 'power', name='uq_item_unique_combo'),
    #)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slot = Column(Enum(SlotType), nullable=False)
    power = Column(Integer, nullable=False)
