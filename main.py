from fastapi import FastAPI
from app.data import Prompt, GenericResponse, Tables, ModelResponse
from app.schema import Schema
from app.interaction import query_model

app = FastAPI()


@app.get("/")
def health():
    return {
        "message": "OK",
    }


@app.get("/schema", response_model=GenericResponse[Tables])
def schema():
    return GenericResponse[Tables](
        message="Success",
        data=Schema.table_data
    )


@app.post("/ask")
def ask(prompt: Prompt):
    result = query_model(prompt.question)

    return GenericResponse[ModelResponse](
        message="Success",
        data=result
    )
