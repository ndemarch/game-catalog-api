from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class SlotType(str, enum.Enum):
    helmet = "Helmet"
    armour = "Armour"
    gloves = "Gloves"
    boots = "Boots"
    weapon = "Weapon"
    shield = "Shield"

class Loadout(Base):
    __tablename__ = "loadouts"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    item_name = Column(String(255), nullable=False)
    slot = Column(Enum(SlotType), nullable=False)
    power = Column(Integer, nullable=False)

    #character = relationship("Character", back_populates="loadouts")
