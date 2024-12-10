from .intent_response import IntentResponse
from app.models import Lecturer

class AskLecturerData(IntentResponse):
    name = "ask_lecturer_data"
    valid_mode = ["list"]
    valid_entities = { 
        "major": "major",
        "faculty": "faculty",
    }
    valid_groupby = []
    model = Lecturer
    aggregate_field = "id"

    def get_list_map(self, row):
        return {
            "id": row.id,
            "nidn": row.nidn,
            "name": row.name,
            "major": row.major,
            "faculty": row.faculty,
        }