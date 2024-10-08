from fastapi import FastAPI
from app.data import Prompt

app = FastAPI()

@app.get('/')
def health():
    return {
        'message': 'OK',
    }

@app.post("/ask")
def ask(prompt: Prompt):
    return {}

