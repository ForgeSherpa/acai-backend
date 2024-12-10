from .intent_response import IntentResponse
from app.models import LecturerResearch


class AskResearchData(IntentResponse):
    name = "ask_research_data"
    valid_mode = ["count", "list"]
    valid_entities = {
        "year": "publication_date",
        "year_range": "range:publication_date",
        "major": "lecturer__major",
        "publication_type": "publication_type",
        "faculty": "lecturer__faculty",
    }
    valid_groupby = [
        "publication_date",
        "publication_type",
    ]
    model = LecturerResearch
    aggregate_field = "id"
    major: str = None
    group_by="publication_date"

    def get_list_map(self, row):
        return {
            "id": row.id,
            "title": row.title,
            "publication_date": row.publication_date,
            "publication_type": row.publication_type,
            "lecturer": {
                "name": row.lecturer.name,
                "major": row.lecturer.major,
            }
            if row.lecturer is not None
            else None,
        }
