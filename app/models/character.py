from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class ClassType(str, enum.Enum):
    warrior = "Warrior"
    mage = "Mage"
    rogue = "Rogue"
    healer = "Healer"
    ranger = "Ranger"
    archer = "Archer"

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    level = Column(Integer, default=1, nullable=False)
    class_type = Column(Enum(ClassType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #loadouts = relationship("Loadout", back_populates="character")
