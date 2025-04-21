from pydantic import BaseModel, field_validator
from app.models.items import SlotType


class ItemBase(BaseModel):
    name: str
    slot: SlotType
    power: int

    @field_validator("slot", mode="before")
    @classmethod
    def normalize_enum(cls, v):
        if isinstance(v, SlotType):
            return v
        try:
            return SlotType[v.strip().lower()]
        except KeyError:
            valid_slots = ', '.join([slot.name for slot in SlotType])
            raise ValueError(f"Invalid slot_type: {v}. Valid options are: {valid_slots}")
        

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    model_config = {
        "from_attributes": True
    }
