from pydantic import BaseModel, field_validator
from datetime import datetime
from app.models.character import ClassType

class CharacterBase(BaseModel):
    name: str
    level: int
    class_type: ClassType

    @field_validator("class_type", mode="before")
    @classmethod
    def normalize_enum(cls, v):
        if isinstance(v, ClassType):
            return v
        for member in ClassType:
            if member.value.lower() == str(v).lower():
                return member
        raise ValueError(f"Invalid class_type: {v}")
        

class CharacterCreate(CharacterBase):
    pass

class CharacterOut(CharacterBase):
    id: int
    abilities: dict
    loadout: dict
    created_at: datetime
    updated_at: datetime
    model_config = {
        "from_attributes": True
    }
