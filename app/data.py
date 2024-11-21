from pydantic import BaseModel
from typing import Any

class Prompt(BaseModel):
    question: str

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
