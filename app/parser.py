from sqlalchemy import select, func, Numeric
from typing import Any
from .data import ModelResponse
from .database import SessionLocal, Base
from .models import Student

class IntentResponse:
    model: Any # Base (the model class extend to) is type of variable so it won't work.
    mode: str
    group_by: str
    valid_mode = []
    valid_entities = {}
    valid_groupby = []
    
    def __init__(self, entities: dict[str, Any], group_by: str = None) -> None:
        self.entities = {self.valid_entities.get(k): v for k, v in entities.items() if self.valid_entities.get(k) is not None}
        self.mode = entities['mode']
        if self.mode not in self.valid_mode:
            raise ValueError(f'Invalid mode value, available values: {self.valid_mode}')

        if group_by is not None and group_by not in self.valid_groupby:
            raise ValueError(f'Invalid group by value, available values: {self.valid_groupby}')
        self.group_by = getattr(Base, group_by) if group_by is not None else None

    def run(self):
        pass

# supported mode: avg, sum, list
# if avg = it will return the average gpa based on the given conditions
# if sum = it will return the total gpa based on the given conditions
# if list = it will return the list of all students based on the given conditions
# supported group_by: generation, status, graduation_year, graduation_semester, faculty
class AskIpkData(IntentResponse):
    model = Student
    mode: str
    group_by: str
    valid_mode = ['avg', 'sum', 'list']
    valid_entities = {'year': 'graduation_year', 'major': 'faculty'}
    valid_groupby = ['generation', 'status', 'graduation_year', 'graduation_semester', 'faculty']

    def run(self):
        if self.mode == 'list':
            return self.list()

        return self.aggregate()

    def list(self):
        with SessionLocal() as db:
            stmt = select(Student).filter_by(**self.entities)

            result = db.scalars(stmt).all()

            return [{
                'id': row.id,
                'name': row.name,
                'faculty': row.faculty,
                'generation': row.generation,
                'gpa': row.gpa,
                'status': row.status,
                'graduation_year': row.graduation_year,
                'graduation_semester': row.graduation_semester,
            } for row in result]


    def aggregate(self):
        modes = {
            'avg': func.cast(func.avg(Student.gpa), Numeric(10, 2)),
            'sum': func.cast(func.sum(Student.gpa), Numeric(10, 2)),
        }

        with SessionLocal() as db:
            selects = [modes[self.mode]]

            if self.group_by is not None:
                selects.append(self.group_by)

            query = select(*selects).filter_by(**self.entities)

            if self.group_by is not None:
                query = query.group_by(getattr(Student, self.group_by))

            result = db.execute(query).all()

            return [float(row[0]) for row in result] if self.group_by is None else {row[1]: float(row[0]) for row in result}

class Parser:
    def __init__(self, query: ModelResponse):
        self.query = query
        self.intents: dict[str, IntentResponse] = {
            # 'ask_graduation_data': self.ask_graduation_data,
            # 'ask_research_data': self.ask_research_data,
            # 'ask_activity_data': self.ask_activity_data,
            'ask_ipk_data': AskIpkData,
        }

    def parse(self, mode: str, group_by: str = None, page: int = 1):
        return self.intents[self.query.intent](self.query.entities, mode, group_by).run()
