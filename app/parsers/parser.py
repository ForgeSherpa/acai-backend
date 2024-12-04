from fastapi.responses import JSONResponse
from ..data import ModelResponse, ErrorResponse
from .ask_ipk_data import AskIpkData
from .ask_graduation_data import AskGraduationData
from .ask_research_data import AskResearchData
from .ask_activity_data import AskActivityData
from .ask_lecturer_data import AskLecturerData
from .intent_response import AdvancedIntentResponse
from .data_empty_error import DataEmptyError


class Parser:
    query: ModelResponse
    intents: dict[str, AdvancedIntentResponse]

    def __init__(self, query: ModelResponse):
        self.query = query
        self.intents: dict[str, AdvancedIntentResponse] = {
            "ask_graduation_data": AskGraduationData,
            "ask_research_data": AskResearchData,
            "ask_activity_data": AskActivityData,
            "ask_ipk_data": AskIpkData,
            "ask_lecturer_data": AskLecturerData,
        }

    def parse(self, mode: str, group_by: str = None, page: int = None):
        page = page or 1

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
            return JSONResponse(
                status_code=400,
                content=ErrorResponse(
                    message=str(e),
                    context={
                        "intent": self.query.intent,
                        "entities": self.query.entities,
                        "mode": mode,
                        "group_by": group_by,
                        "page": page,
                    },
                ).to_json(),
            )
        except DataEmptyError as e:
            return JSONResponse(
                status_code=404,
                content=ErrorResponse(
                    message=str(e),
                    context={
                        **e.meta,
                        "model": {
                            "intent": self.query.intent,
                            "entities": self.query.entities,
                        },
                        "raw_query": e.raw_query,
                    },
                ).to_json(),
            )
