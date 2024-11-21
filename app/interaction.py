from .data import ModelResponse,ModelResponseCoordinates

def query_model(q: str) -> ModelResponse:
    # WIP: Implement the query model function based on AI model response.
    return ModelResponse(
        intent="data_kelulusan",
        entities={
            "year": 2021,
        }
    )
