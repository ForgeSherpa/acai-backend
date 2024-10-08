# AcAI Backend

FastAPI(+SQLAlchemy) Powered Backend Service for AcAI Service

## Requirements

- Python 3.10+ (preferable 3.12)

## Installation

Bash:

```bash
python -m venv .
source bin/activate # depends on the OS, in Windows for instance it become `Scripts\activate`.
pip install -r requirements.txt
python cli.py migrate:sqlite
python cli.py migrate 
```

## Running

```bash
fastapi dev main.py
```

## Documentation

The Backend Service is made using OpenAPI 3.0 standard. The Interactive SwaggerUI is accesible within `/docs` endpoint.