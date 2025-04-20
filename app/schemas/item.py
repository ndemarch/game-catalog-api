from pydantic import BaseModel, field_validator
from app.models.items import SlotType


class ItemBase(BaseModel):
    name: str
    slot: SlotType
    power: int

    #@field_validator("type", mode="before")
    #@classmethod
    #def normalize_enum(cls, v):
    #    if isinstance(v, SlotType):
    #        return v
    #    for member in SlotType:
    #        if member.value.lower() == str(v).lower():
    #            return member
    #    raise ValueError(f"Invalid slot_type: {v}")
        

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    model_config = {
        "from_attributes": True
    }
