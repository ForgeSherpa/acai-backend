from typing import Any

class DataEmptyError(Exception):
    applied_entities: list[dict[str, Any]]
    applied_range: list[dict[str, Any]]
    applied_relation: dict[str, Any]
    applied_year: tuple[str, int]

    def __init__(self, entities: list[dict[str, Any]], year: tuple[str, int], relation: dict[str, Any], range: list[dict[str, Any]]):
        super().__init__("Data not found. Please review your request.")

        self.applied_entities = entities
        self.applied_year = year
        self.applied_relation = relation
        self.applied_range = range