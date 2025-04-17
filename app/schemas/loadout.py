from pydantic import BaseModel, field_validator
from app.models.loadout import SlotType


class LoadoutBase(BaseModel):
    item_name: str
    slot: SlotType
    power: int

    #@field_validator("slot", mode="before")
    #@classmethod
    #def normalize_enum(cls, v):
    #    return SlotType[v.capitalize()]
        

class LoadoutCreate(LoadoutBase):
    character_id: int

class LoadoutOut(LoadoutBase):
    id: int
    character_id: int
    model_config = {
        "from_attributes": True
    }
