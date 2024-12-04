from typing import Any


class DataEmptyError(Exception):
    meta: dict[str, Any]
    raw_query: str

    def __init__(self, meta: dict[str, Any], raw_query: str):
        super().__init__("Data not found. Please review your request.")

        self.meta = meta
        self.raw_query = raw_query
