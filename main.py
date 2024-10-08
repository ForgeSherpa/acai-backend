from fastapi import FastAPI
from app.data import Prompt, Schema, Tables, TableDefinition, Column

app = FastAPI()


@app.get("/")
def health():
    return {
        "message": "OK",
    }


@app.get("/schema", response_model=Schema)
def schema():
    return Schema(
        message="Success",
        data=Tables(
            tables=[
                TableDefinition(
                    name="lecturers",
                    columns=[
                        Column(name="id", type="int"),
                        Column(name="nidn", type="int"),
                        Column(name="name", type="str"),
                    ],
                    relations=["researches"],
                ),
                TableDefinition(
                    name="lecturer_researches",
                    columns=[
                        Column(name="id", type="int"),
                        Column(name="nidn", type="int"),
                        Column(name="title", type="str"),
                        Column(name="publication_date", type="date"),
                        Column(name="publication_type", type="str"),
                        Column(name="publication_detail", type="str"),
                    ],
                    relations=["lecturer"],
                ),
                TableDefinition(
                    name="students",
                    columns=[
                        Column(name="id", type="int"),
                        Column(name="name", type="str"),
                        Column(name="faculty", type="str"),
                        Column(name="generation", type="int"),
                        Column(name="gpa", type="float"),
                        Column(name="status", type="str"),
                        Column(name="graduation_year", type="int"),
                        Column(name="graduation_semester", type="int"),
                    ],
                    relations=["activities"],
                ),
                TableDefinition(
                    name="student_activities",
                    columns=[
                        Column(name="id", type="int"),
                        Column(name="student_id", type="int"),
                        Column(name="bank_id", type="int"),
                        Column(name="name", type="str"),
                        Column(name="type", type="str"),
                        Column(name="date", type="date"),
                    ],
                    relations=["student"],
                ),
            ]
        ),
    )


@app.post("/ask")
def ask(prompt: Prompt):
    return {}
