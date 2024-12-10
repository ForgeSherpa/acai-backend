from .intent_response import IntentResponse
from app.models import StudentActivity

class AskActivityData(IntentResponse):
    name = "ask_activity_data"
    valid_mode = ["count", "list"]
    valid_entities = {
        "year": "date",
        "year_range": "range:date",
        "major": "student__major",
        "faculty": "student__faculty",
        "activity_level": "type",
    }
    valid_groupby = [
        "date",
        "type",
    ]
    model = StudentActivity
    aggregate_field = "id"
    group_by="date"

    def get_list_map(self, row):
        return {
            "id": row.id,
            "name": row.name,
            "type": row.type,
            "date": row.date,
            "student": {
                "name": row.student.name,
                "major": row.student.major,
                "faculty": row.student.faculty,
            }
        }