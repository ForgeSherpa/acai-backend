from .data import ModelResponse
import requests

def query_model(q: str) -> ModelResponse:
    res = requests.post("http://localhost:5005/model/parse", json={"text": q})
    data = res.json()

    intent = data['intent']['name']
    entities = {entity['entity']: entity['value'] for entity in data['entities']}

    print(f"query_model intent: {intent}")
    print(f"query_model entities: {entities}")

    return ModelResponse(
        intent=intent,
        entities=entities
    )
