from pydantic import BaseModel

class Prompt(BaseModel):
    question: str

class FilterLookup(BaseModel):
    column: str
    operator: str
    value: str

class TableLookup(BaseModel):
    name: str
    columns: list[str]
    filters: list[FilterLookup]
    relations: list[str]

"""
tables: [
    {
        "name": "lecturers",
        "columns": ["*"],
        "relations": ["relationship if any"],
        "filters": [
            {
                "column": "nidn",
                "operator": "=",
                "value": "12345"
            },
            {
                "column": "date,
                "operator": ">",
                "value": "2021-01-01"
            }
        ]
    }
]
"""
class ModelResponse(BaseModel):
    tables: list[TableLookup]

class TableDefinition(BaseModel):
    name: str
    columns: list[str]
    relations: list[str]

class Tables(BaseModel):
    tables: list[TableDefinition]

"""
{
    "message": "Success",
    "data": {
        "tables": [
            {
                "name": "lectures",
                "columns": ["id", "nidn", "name"],
                "relations": ["researches"],
            }
        ]
    }
}
"""
class Schema(BaseModel):
    message: str
    data: Tables