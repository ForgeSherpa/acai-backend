from .intent_response import IntentResponse
from app.models import Student


# supported mode: count, list
# if count = it will return the entire count of student on the given conditions
# if list = it will return the list of all students based on the given conditions
class AskGraduationData(IntentResponse):
    name = "ask_graduation_data"
    valid_mode = ["count", "list"]
    valid_entities = {
        "year": "graduation_year",
        "major": "faculty",
        "year_range": "range:graduation_year",
        "faculty": "faculty",
        "period": "graduation_semester",
    }
    valid_groupby = [
        "generation",
        "status",
        "graduation_year",
        "graduation_semester",
        "faculty",
    ]
    model = Student
    aggregate_field = "id"

    def get_list_map(self, row):
        return {
            "id": row.id,
            "name": row.name,
            "faculty": row.faculty,
            "generation": row.generation,
            "gpa": row.gpa,
            "status": row.status,
            "graduation_year": row.graduation_year,
            "graduation_semester": row.graduation_semester,
        }

    def get_aggregate_result(self, result):
        return (
            [float(row[0]) for row in result]
            if len(result) > 1
            else float(result[0][0])
            if self.group_by is None
            else {row[1]: float(row[0]) for row in result}
        )
