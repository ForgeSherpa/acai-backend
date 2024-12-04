from typing import Any
import re
from app.data import AskResponse
from app.database import SessionLocal
from sqlalchemy import select, func, Select, Numeric, extract
from abc import ABC, abstractmethod
from .data_empty_error import DataEmptyError


class RangeFilter[T]:
    field: str
    start: T
    end: T

    def __init__(self, field: str, start: T, end: T) -> None:
        self.field = field
        self.start = start
        self.end = end

    def to_dict(self):
        return {
            "field": self.field,
            "start": self.start,
            "end": self.end,
        }


class RelationshipFilter[T]:
    relationship: str
    field: str
    value: T

    def __init__(self, relationship: str, field: str, value: T) -> None:
        self.relationship = relationship
        self.field = field
        self.value = value

    def to_dict(self):
        return {
            "relationship": self.relationship,
            "field": self.field,
            "value": self.value,
        }


class AdvancedIntentResponse(ABC):
    name: str
    mode: str
    group_by: str
    valid_mode: list[str] = []
    valid_entities: dict[str, str] = {}
    valid_groupby: list[str] = []
    page: int
    per_page: int = 15
    meta: dict[str, Any]
    pagination_meta: dict[str, Any]
    range_filter: list[RangeFilter] = []
    year_filter: tuple[str, int] = None
    entities: dict[str, Any] = {}
    relationships: list[RelationshipFilter] = []

    def __init__(
        self,
        entities: dict[str, Any],
        group_by: str = None,
        page: int = 1,
        mode: str = None,
    ) -> None:
        # reset all the property to the default value
        self.entities = {}
        self.relationships = []
        self.range_filter = []

        # map the entities to the valid entities and filters.
        for k, v in entities.items():
            valid_entity = self.valid_entities.get(k)

            if valid_entity is None:
                continue

            if valid_entity.startswith("range:"):
                field = valid_entity.split(":")[1]
                regex = r"(\d{4}) - (\d{4})"
                match = re.match(regex, v)

                if not match:
                    raise ValueError(f"Invalid range format for {k}")

                start, end = match.groups()

                if "date" in valid_entity:
                    start = f"{start}-01-01"
                    end = f"{end}-12-31"

                self.range_filter.append(RangeFilter(field, start=start, end=end))
            elif "__" in valid_entity:
                relationship, field = valid_entity.split("__")
                self.relationships.append(RelationshipFilter(relationship, field, v))
            elif "date" in valid_entity:
                self.year_filter = (valid_entity, int(v))
            else:
                self.entities[valid_entity] = v

        # infer mode from the model, if not provided fallback to parameter mode
        # if still not provided, fallback to the first valid mode
        self.mode = entities.get("mode") or mode or self.valid_mode[0]

        # Forcefully set the mode to count if both count and sum not available
        # This is due to the limitation of the current model implementation unable to
        # infer mode = count. Therefore we need to force it.
        # For future improvement, we can infer the mode based on the model
        has_count = False
        has_sum = False

        for mode in self.valid_mode:
            if mode == "count":
                has_count = True
            elif mode == "sum":
                has_sum = True

        if has_count and not has_sum and mode == "sum":
            self.mode = "count"

        if self.mode not in self.valid_mode:
            raise ValueError(f"Invalid mode value, available values: {self.valid_mode}")

        if group_by is not None and group_by not in self.valid_groupby:
            raise ValueError(
                f"Invalid group by value, available values: {self.valid_groupby}"
            )

        self.group_by = group_by

        self.page = page
        self.meta = {
            "group_by": group_by,
            "mode": self.mode,
            "entities": self.entities,
            "intent": self.name,
            "available_group_by": self.valid_groupby,
            "available_mode": self.valid_mode,
            "available_entities": self.valid_entities,
            "range_filter": [filter.to_dict() for filter in self.range_filter],
            "year_filter": self.year_filter,
            "relationship_filter": [filter.to_dict() for filter in self.relationships],
        }
        self.pagination_meta = {
            "page": self.page,
            "per_page": self.per_page,
        }

    def run(self):
        if self.mode == "list":
            return self.list()

        return self.aggregate()

    def with_pagination(self, data: Any, total_page: int) -> AskResponse:
        return AskResponse(
            data=data,
            meta={**self.meta, **self.pagination_meta, "total_page": total_page},
        )

    def with_meta(self, data: Any) -> AskResponse:
        return AskResponse(data=data, meta=self.meta)

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def aggregate(self):
        pass


# The actual parser implementation actually lives here.
# In this class lies the core logic of the parser involving filtering relationship, year, year range, entities filter
# pagination, group by, and much more (via bind_* and get_query methods).
# It may take a while to understand this parser, and take a lot of time to debug. So... good luck.
# I mean it kinda worth it, all you need to do is to extend this class and override some methods and properties
# after that everything will work out of the box (probably).
class IntentResponse(AdvancedIntentResponse):
    model: Any
    primary_id: str = "id"
    aggregate_field: str

    @abstractmethod
    def get_list_map(self, row):
        pass

    def get_aggregate_result(self, result):
        if self.group_by is None:
            return (
                [float(row[0]) for row in result]
                if len(result) > 1
                else float(result[0][0])
            )

        return {row[1]: float(row[0]) for row in result}

    def get_bind_queries(self, with_pagination: bool = True) -> list:
        return [
            self.bind_entities,
            self.bind_relationship_filter,
            self.bind_range_filter,
            self.bind_year_filter,
            self.bind_group_by,
        ] + ([self.bind_pagination] if with_pagination else [])

    def get_query(self, select: Select, with_pagination: bool = True):
        for bind_query in self.get_bind_queries(with_pagination=with_pagination):
            select = bind_query(select)

        return select

    def get_total_page(self, db):
        total_items = db.execute(
            self.get_query(
                select(func.count(getattr(self.model, self.primary_id))),
                with_pagination=False,
            )
        ).scalar()

        return (total_items // self.per_page) + 1

    def bind_range_filter(self, select: Select):
        if len(self.range_filter) > 0:
            for filter in self.range_filter:
                select = select.filter(
                    getattr(self.model, filter.field).between(filter.start, filter.end)
                )

        return select

    def bind_group_by(self, select: Select):
        # if the mode is list, we don't need to group by
        # group_by only supported in non-list mode
        if self.mode == "list":
            return select

        if self.group_by is not None:
            if "date" in self.group_by:
                group_by_column = extract("year", getattr(self.model, self.group_by))
            else:
                group_by_column = getattr(self.model, self.group_by)

            select = select.group_by(group_by_column)

        return select

    def bind_entities(self, select: Select):
        for entity, value in self.entities.items():
            select = select.where(getattr(self.model, entity).ilike(value))

        return select

    def bind_pagination(self, select: Select):
        offset = (self.page - 1) * self.per_page
        return select.offset(offset).limit(self.per_page)

    def bind_year_filter(self, select: Select):
        if self.year_filter is not None:
            return select.where(
                extract("year", getattr(self.model, self.year_filter[0]))
                == self.year_filter[1]
            )

        return select

    def bind_relationship_filter(self, select: Select):
        for filter in self.relationships:
            select = select.where(
                getattr(self.model, filter.relationship).has(
                    **{filter.field: filter.value}
                )
            )

        return select

    def bind_group_by_select(self):
        if self.group_by is not None:
            if "date" in self.group_by:
                return extract("year", getattr(self.model, self.group_by))

            return getattr(self.model, self.group_by)

        return None

    def list(self):
        with SessionLocal() as db:
            stmt = self.get_query(select(self.model))
            result = db.scalars(stmt).all()

            if len(result) <= 0:
                raise DataEmptyError(
                    entities=self.entities,
                    year=self.year_filter,
                    relation=self.relationships,
                    range=self.range_filter,
                )

            data = [self.get_list_map(row) for row in result]

            return self.with_pagination(data, self.get_total_page(db))

    def aggregate(self):
        if self.aggregate_field is None:
            raise ValueError("Aggregate field is not defined")

        with SessionLocal() as db:
            modes = {
                "avg": func.cast(
                    func.avg(getattr(self.model, self.aggregate_field)), Numeric(10, 2)
                ),
                "sum": func.cast(
                    func.sum(getattr(self.model, self.aggregate_field)), Numeric(10, 2)
                ),
                "count": func.count(getattr(self.model, self.aggregate_field)),
            }

            query = self.get_query(
                select(
                    *[
                        modes[self.mode],
                        self.bind_group_by_select(),
                    ]
                ),
                with_pagination=False,
            )

            result = db.execute(query).all()

            if len(result) <= 0 or result[0][0] is None:
                raise DataEmptyError(
                    entities=self.entities,
                    year=self.year_filter,
                    relation=self.relationships,
                    range=self.range_filter,
                )

            data = self.get_aggregate_result(result)

            return self.with_meta(data)
