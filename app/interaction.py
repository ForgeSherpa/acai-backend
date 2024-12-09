from .data import ModelResponse
import requests
import functools
from time import time

@functools.lru_cache()
def request_model(q: str, ttl_hash=None):
    res = requests.post("http://localhost:5005/model/parse", json={"text": q})
    return res.json()

def query_model(q: str) -> ModelResponse:
    # cache 5 minutes
    data = request_model(q, ttl_hash=round(time() / 300))

    intent = data['intent']['name']
    entities = {entity['entity']: entity['value'] for entity in data['entities']}

    print(f"query_model intent: {intent}")
    print(f"query_model entities: {entities}")

    return ModelResponse(
        intent=intent,
        entities=entities
    )
