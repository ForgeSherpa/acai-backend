from fastapi.responses import JSONResponse
from sqlalchemy import select, func, Numeric
from typing import Any
from .data import ModelResponse, AskResponse, ErrorResponse
from .database import SessionLocal
from .models import Student


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

    def __init__(
        self,
        entities: dict[str, Any],
        group_by: str = None,
        page: int = 1,
        mode: str = None,
    ) -> None:
        self.entities = {
            self.valid_entities.get(k): v
            for k, v in entities.items()
            if self.valid_entities.get(k) is not None
        }

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
        }
        self.pagination_meta = {
            "page": self.page,
            "per_page": self.per_page,
        }

    def run(self):
        pass

    def with_pagination(self, data: Any, total_page: int) -> AskResponse:
        return AskResponse(
            data=data,
            meta={**self.meta, **self.pagination_meta, "total_page": total_page},
        )

    def with_meta(self, data: Any) -> AskResponse:
        return AskResponse(data=data, meta=self.meta)


# supported mode: avg, sum, list
# if avg = it will return the average gpa based on the given conditions
# if sum = it will return the total gpa based on the given conditions
# if list = it will return the list of all students based on the given conditions
# supported group_by: generation, status, graduation_year, graduation_semester, faculty
class AskIpkData(IntentResponse):
    name = "ask_ipk_data"
    valid_mode = ["avg", "sum", "list"]
    valid_entities = {"year": "graduation_year", "major": "faculty"}
    valid_groupby = [
        "generation",
        "status",
        "graduation_year",
        "graduation_semester",
        "faculty",
    ]

    def run(self):
        if self.mode == "list":
            return self.list()

        return self.aggregate()

    def list(self):
        with SessionLocal() as db:
            stmt = select(Student).filter_by(**self.entities)

            # result = db.scalars(stmt).all()
            offset = (self.page - 1) * self.per_page
            stmt = stmt.offset(offset).limit(self.per_page)
            result = db.scalars(stmt).all()
            total_page = db.execute(
                select(func.count(Student.id)).filter_by(**self.entities)
            ).scalar()

            data = [
                {
                    "id": row.id,
                    "name": row.name,
                    "faculty": row.faculty,
                    "generation": row.generation,
                    "gpa": row.gpa,
                    "status": row.status,
                    "graduation_year": row.graduation_year,
                    "graduation_semester": row.graduation_semester,
                }
                for row in result
            ]

            return self.with_pagination(data, total_page)

    def aggregate(self):
        modes = {
            "avg": func.cast(func.avg(Student.gpa), Numeric(10, 2)),
            "sum": func.cast(func.sum(Student.gpa), Numeric(10, 2)),
        }

        with SessionLocal() as db:
            selects = [modes[self.mode]]

            group_by_column = getattr(Student, self.group_by) if self.group_by else None

            if self.group_by is not None:
                selects.append(group_by_column)

            query = select(*selects).filter_by(**self.entities)

            if self.group_by is not None:
                query = query.group_by(group_by_column)

            result = db.execute(query).all()

            data = (
                [float(row[0]) for row in result]
                if self.group_by is None
                else {row[1]: float(row[0]) for row in result}
            )

            return self.with_meta(data)


class Parser:
    query: ModelResponse
    intents: dict[str, IntentResponse]

    def __init__(self, query: ModelResponse):
        self.query = query
        self.intents: dict[str, IntentResponse] = {
            # 'ask_graduation_data': self.ask_graduation_data,
            # 'ask_research_data': self.ask_research_data,
            # 'ask_activity_data': self.ask_activity_data,
            "ask_ipk_data": AskIpkData,
        }

    def parse(self, mode: str, group_by: str = None, page: int = 1):
        try:
            if self.query.intent not in self.intents:
                raise ValueError(f"Intent {self.query.intent} is not supported")

            return self.intents[self.query.intent](
                entities=self.query.entities,
                group_by=group_by,
                page=page,
                mode=mode,
            ).run()
        except ValueError as e:
            return JSONResponse(status_code=400, content=ErrorResponse(
                message=str(e),
                context={
                    "intent": self.query.intent,
                    "entities": self.query.entities,
                    "mode": mode,
                    "group_by": group_by,
                    "page": page,
                },
            ).to_json())
