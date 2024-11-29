from pydantic import BaseModel, Field
from typing import Any

"""
{
    "question": "Saya ingin tahu data kelulusan untuk tahun 2022.",
    "mode": "list",
    "group_by": "year",
    "page": 1
}
"""
class Prompt(BaseModel):
    question: str
    mode: str = Field(None)
    group_by: str = Field(None)
    page: int = Field(None)

"""
{
    "intent": "data_kelulusan",
    "entities": {
        "year_start": 2021,
        "year_end": 2024
    }
}
"""
class ModelResponse(BaseModel):
    intent: str
    entities: dict[str, Any]

class Column(BaseModel):
    name: str
    type: str

class TableDefinition(BaseModel):
    name: str
    columns: list[Column]
    relations: list[str]

"""
[
    {
        "name": "lectures",
        "columns": [
            {
                "name": "id",
                "type": "int"
            },
            {
                "name": "nidn",
                "type": "int"
            },
            {
                "name": "name",
                "type": "str"
            }
        ],
        "relations": ["researches"],
    }
]
"""
class Tables(BaseModel):
    tables: list[TableDefinition]

class GenericResponse[T](BaseModel):
    message: str
    data: T

class AskResponse(BaseModel):
    data: Any
    meta: dict[str, Any]

class ErrorResponse(BaseModel):
    message: str
    context: dict[str, Any]

    def to_json(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "context": self.context
        }