from .data import ModelResponse
import requests

def query_model(q: str) -> ModelResponse:
    data = {
        "text": q
    }
    res = requests.post("http://localhost:5005/model/parse", json=data)
    data = res.json()

    return ModelResponse(
        intent=data['intent']['name'],
        entities = {entity['entity']: entity['value'] for entity in data['entities']}
    )