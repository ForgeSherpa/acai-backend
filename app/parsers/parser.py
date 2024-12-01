from fastapi.responses import JSONResponse
from ..data import ModelResponse, ErrorResponse
from .ask_ipk_data import AskIpkData
from .ask_graduation_data import AskGraduationData
from .intent_response import IntentResponse


class Parser:
    query: ModelResponse
    intents: dict[str, IntentResponse]

    def __init__(self, query: ModelResponse):
        self.query = query
        self.intents: dict[str, IntentResponse] = {
            'ask_graduation_data': AskGraduationData,
            # 'ask_research_data': self.ask_research_data,
            # 'ask_activity_data': self.ask_activity_data,
            "ask_ipk_data": AskIpkData,
            # "ask_lecuturer_data": AskIpkData,
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
