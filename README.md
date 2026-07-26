# PsychoNavigatorAPI

PsychoNavigatorAPI is a FastAPI backend for the Psycho Navigator project. The
service exposes API routes for health checks and psychological test data.

## Stack

- Python 3.14
- FastAPI
- Pydantic / Pydantic Settings
- uv
- Ruff
- pytest

## Requirements

- Python 3.14
- uv

## Setup

Install dependencies:

```powershell
uv sync --dev
```

Create a local environment file from the example:

```powershell
Copy-Item .env.example .env
```

## Local Run

Start the development server:

```powershell
fastapi dev src/psycho_navigator/main.py
```

After startup, the API is available at:

- Swagger UI: http://127.0.0.1:8000/docs
- Health endpoint: http://127.0.0.1:8000/health/

## Checks

Run Ruff:

```powershell
uv run ruff check .
```

Run tests:

```powershell
uv run pytest
```
