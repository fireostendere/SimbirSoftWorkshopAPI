# data/model.py

from typing import List
from pydantic import BaseModel, Field


class AdditionRequest(BaseModel):
    additional_info: str = Field(..., json_schema_extra={'example': "Дополнительные сведения"})
    additional_number: int = Field(..., json_schema_extra={'example': 123})


class EntityAdd(BaseModel):
    addition: AdditionRequest
    important_numbers: List[int] = Field(..., json_schema_extra={'example': [42, 87, 15]})
    title: str = Field(..., json_schema_extra={'example': "Заголовок сущности"})
    verified: bool = Field(..., json_schema_extra={'example': True})


class EntityRequest(BaseModel):
    addition: AdditionRequest
    important_numbers: List[int] = Field(..., json_schema_extra={'example': [42, 87, 15]})
    title: str = Field(..., json_schema_extra={'example': "Заголовок сущности"})
    verified: bool = Field(..., json_schema_extra={'example': True})


class AdditionResponse(BaseModel):
    additional_info: str = Field(..., json_schema_extra={'example': "Дополнительные сведения"})
    additional_number: int = Field(..., json_schema_extra={'example': 123})
    id: int = Field(..., json_schema_extra={'example': 1})


class EntityResponse(BaseModel):
    addition: AdditionResponse
    id: int = Field(..., json_schema_extra={'example': 1})
    important_numbers: List[int] = Field(..., json_schema_extra={'example': [42, 87, 15]})
    title: str = Field(..., json_schema_extra={'example': "Заголовок сущности"})
    verified: bool = Field(..., json_schema_extra={'example': True})


class EntitiesResponse(BaseModel):
    entity: List[EntityResponse]