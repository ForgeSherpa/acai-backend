from pydantic import BaseModel, field_validator

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

    @field_validator('tables')
    @classmethod
    def table_should_unique(self, v: list[TableLookup]) -> list[TableLookup]:
        table_names = [table.name for table in v]

        if len(table_names) != len(set(table_names)):
            raise ValueError("Table names should be unique")

        return v

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