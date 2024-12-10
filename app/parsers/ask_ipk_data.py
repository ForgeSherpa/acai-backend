from .intent_response import IntentResponse
from app.models import Student


# supported mode: avg, sum, list
# if avg = it will return the average gpa based on the given conditions
# if sum = it will return the total gpa based on the given conditions
# if list = it will return the list of all students based on the given conditions
# supported group_by: generation, status, graduation_year, graduation_semester, faculty
class AskIpkData(IntentResponse):
    name = "ask_ipk_data"
    valid_mode = ["avg", "sum", "list"]
    valid_entities = {
        "year": "graduation_year",
        "major": "major",
        "year_range": "range:graduation_year",
        "faculty": "faculty",
        "period": "graduation_semester",
        "cohort": "generation",
    }
    valid_groupby = [
        "generation",
        "graduation_year",
        "graduation_semester",
        "faculty",
    ]
    model = Student
    aggregate_field = "gpa"
    group_by = "graduation_year"

    def run(self):
        if self.mode == "list":
            return self.list()

        return self.aggregate()

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
