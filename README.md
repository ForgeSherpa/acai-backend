# AcAI Backend

FastAPI(+SQLAlchemy) Powered Backend Service for AcAI Service

## Requirements

- Python 3.10+ (preferable 3.12)

## Installation

Bash:

```bash
python -m venv .
# depends on the OS, please read, no ask: https://docs.python.org/3/library/venv.html
# if too lazy to read, ask ChatGPT.
source bin/activate 
# if fail probably cross platform version constraint issue, please fix it by the lastest one available in your platform
# if you don't know how, ask ChatGPT.
pip install -r requirements.txt
python cli.py migrate:sqlite
python cli.py migrate 
```

## Running

Before running make sure the virtual env already activated (`source bin/activate` by executing this). If not sure, ask ChatGPT.

```bash
python cli.py serve
```

Use above command so version checking can be performed.

## Documentation

The Backend Service is made using OpenAPI 3.0 standard. The Interactive SwaggerUI is accesible within `/docs` endpoint.