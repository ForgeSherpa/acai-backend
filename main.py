from fastapi import FastAPI
from app.data import Prompt, GenericResponse, Tables 
from app.schema import Schema

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
    return {}
