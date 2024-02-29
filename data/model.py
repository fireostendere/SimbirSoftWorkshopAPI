from typing import Dict, Any, List
from pydantic import BaseModel, Field


class EntityAdd(BaseModel):
    custom_properties: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.custom_properties.update({
            "addition": self.custom_properties.get(
                "addition", {"additional_info": "Дополнительные сведения", "additional_number": 123}),
            "important_numbers": self.custom_properties.get("important_numbers", [42, 87, 87, 87, 15]),
            "title": self.custom_properties.get("title", "Заголовок сущности"),
            "verified": self.custom_properties.get("verified", True)
        })


class Addition(BaseModel):
    additional_info: str
    additional_number: int
    id: int


class Entity(BaseModel):
    id: int
    addition: dict
    important_numbers: List[int]
    title: str
    verified: bool


class EntitiesResponse(BaseModel):
    entity: List[Entity]
