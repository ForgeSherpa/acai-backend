from .data import ModelResponse
import requests

def query_model(q: str) -> ModelResponse:
    res = requests.post("http://localhost:5005/model/parse", json={"text": q})
    data = res.json()

    return ModelResponse(
        intent=data['intent']['name'],
        entities = {entity['entity']: entity['value'] for entity in data['entities']}
    )