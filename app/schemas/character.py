from pydantic import BaseModel, field_validator
from datetime import datetime
from app.models.character import ClassType

class CharacterBase(BaseModel):
    name: str
    level: int
    class_type: ClassType

    #@field_validator("class_type", mode="before")
    #@classmethod
    #def normalize_enum(cls, v):
    #    return ClassType[v.capitalize()]

class CharacterCreate(CharacterBase):
    pass

class CharacterOut(CharacterBase):
    id: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }
