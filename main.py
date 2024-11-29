from fastapi import FastAPI
from app.data import Prompt, GenericResponse, Tables, AskResponse, ErrorResponse
from app.schema import Schema
from app.interaction import query_model
from app.parser import Parser

app = FastAPI()


@app.get("/", summary="Health check")
def health():
    return {
        "message": "OK",
    }


@app.get(
    "/schema",
    response_model=GenericResponse[Tables],
    summary="Get the schema (deprecated)",
    deprecated=True,
)
def schema():
    return GenericResponse[Tables](message="Success", data=Schema.table_data)


@app.post(
    "/ask",
    response_model=AskResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Ask the model",
    description="Dear FE, 'mode', 'group_by', and 'page' is optional. Use 'page' if 'mode' is 'list'. Usually, 'mode' are inferred by the Model",
)
def ask(prompt: Prompt):
    query = query_model(prompt.question)

    parser = Parser(query)

    result = parser.parse(
        mode=prompt.mode,
        group_by=prompt.group_by,
        page=prompt.page,
    )

    return result
