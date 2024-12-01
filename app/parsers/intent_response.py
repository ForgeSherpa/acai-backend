from typing import Any
import re
from app.data import AskResponse
from app.database import SessionLocal
from app.models import Student
from sqlalchemy import select, func, Select, Numeric


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


class IntentResponse:
    name: str
    mode: str
    group_by: str
    valid_mode = []
    valid_entities = {}
    valid_groupby = []
    page: int
    per_page: int = 15
    meta: dict[str, Any]
    pagination_meta: dict[str, Any]
    range_filter: list[RangeFilter] = []
    entities = {}
    model: Any
    primary_id: str = "id"
    aggregate_field: str

    def __init__(
        self,
        entities: dict[str, Any],
        group_by: str = None,
        page: int = 1,
        mode: str = None,
    ) -> None:
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

                self.range_filter.append(RangeFilter(field, start=start, end=end))
            else:
                self.entities[valid_entity] = v

        # infer mode from the model, if not provided fallback to parameter mode
        # if still not provided, fallback to the first valid mode
        self.mode = entities.get("mode") or mode or self.valid_mode[0]

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

    def get_list_map(self, row):
        pass

    def get_aggregate_result(self, result):
        pass

    def bind_range_filter(self, select: Select):
        if len(self.range_filter) > 0:
            for filter in self.range_filter:
                select = select.filter(
                    getattr(self.model, filter.field).between(filter.start, filter.end)
                )

        return select

    def bind_group_by(self, select: Select):
        if self.group_by is not None:
            group_by_column = getattr(self.model, self.group_by)
            select = select.group_by(group_by_column)

        return select

    def bind_entities(self, select: Select):
        return select.filter_by(**self.entities)

    def list(self):
        with SessionLocal() as db:
            offset = (self.page - 1) * self.per_page
            stmt = (
                self.bind_range_filter(self.bind_entities(select(self.model)))
                .offset(offset)
                .limit(self.per_page)
            )
            result = db.scalars(stmt).all()
            total_items = db.execute(
                self.bind_range_filter(
                    self.bind_entities(select(func.count(self.model.id)))
                )
            ).scalar()

            data = [self.get_list_map(row) for row in result]

            return self.with_pagination(
                data, total_page=(total_items // self.per_page) + 1
            )

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

            query = self.bind_group_by(
                self.bind_range_filter(
                    self.bind_entities(
                        select(
                            *[
                                modes[self.mode],
                                getattr(self.model, self.group_by)
                                if self.group_by
                                else None,
                            ]
                        )
                    )
                )
            )

            result = db.execute(query).all()

            data = self.get_aggregate_result(result)

            return self.with_meta(data)
