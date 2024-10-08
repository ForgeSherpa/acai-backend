from fastapi import FastAPI
from app.data import Prompt, Schema, Tables, TableDefinition

app = FastAPI()

@app.get('/')
def health():
    return {
        'message': 'OK',
    }

@app.get('/schema', response_model=Schema)
def schema():
    return Schema(message='Success', data=Tables(tables=[
        TableDefinition(name='lecturers', columns=['id', 'nidn', 'name'], relations=['researches']),
        TableDefinition(name='lecturer_researches', columns=['id', 'nidn', 'title', 'publication_date', 'publication_type', 'publication_detail'], relations=['lecturer']),
        TableDefinition(name='students', columns=['id', 'name', 'faculty', 'generation', 'gpa', 'status', 'graduation_year', 'graduation_semester'], relations=['activities']),
        TableDefinition(name='student_activities', columns=['id', 'student_id', 'bank_id', 'name', 'type', 'date'], relations=['student']),
    ]))

@app.post("/ask")
def ask(prompt: Prompt):
    return {}

