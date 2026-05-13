# Job Board API

A RESTful backend API that allows employers to create job postings with custom scoring questions, and candidates to apply to jobs. Each application is automatically scored based on the candidate's answers, using a flexible scoring system that supports multiple question types.

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLAlchemy ORM with SQLite (swappable to PostgreSQL)
- **Validation:** Pydantic v2 with email validation and field constraints
- **Testing:** pytest with isolated test database
- **Linting:** Ruff (lint + format), mypy (type checking), pre-commit hooks

## Project Structure

```
app/
├── main.py            # Application entry point, CORS, error handling
├── config.py          # Typed settings via Pydantic BaseSettings
├── database.py        # Engine, session factory, declarative base
├── models.py          # SQLAlchemy ORM models
├── schemas.py         # Pydantic request/response schemas
├── enums.py           # QuestionType enum
├── dependencies.py    # Shared FastAPI dependencies (get_db, get_or_404)
├── routers/
│   ├── jobs.py        # Job CRUD endpoints
│   └── applications.py # Application submission and retrieval
└── services/
    └── scoring.py     # Scoring engine for 4 question types
tests/
├── conftest.py        # Fixtures and test database setup
└── test_api.py        # API and unit tests
```

## Quick Start

One command — creates a virtual environment, installs dependencies, and starts the server:

```bash
./run.sh
```

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

## Manual Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running Tests

```bash
pytest tests/ -v
```

## Makefile

```bash
make setup        # Create venv and install deps
make setup-dev    # Install with dev tools (ruff, mypy, pre-commit)
make run          # Start the dev server
make test         # Run all tests
make lint         # Run linter (ruff)
make format       # Auto-format code (ruff)
make typecheck    # Run type checker (mypy)
make check        # Run lint + typecheck + tests
make clean        # Remove venv, caches, databases
```

## API Endpoints

| Method | Endpoint                        | Description                              |
|--------|---------------------------------|------------------------------------------|
| POST   | `/jobs`                         | Create a job posting with questions      |
| GET    | `/jobs`                         | List all jobs                            |
| GET    | `/jobs/{job_id}`                | Get a specific job                       |
| DELETE | `/jobs/{job_id}`                | Delete a job (cascades)                  |
| POST   | `/jobs/{job_id}/apply`          | Submit an application with answers       |
| GET    | `/applications/{id}`            | View a single application                |
| GET    | `/jobs/{job_id}/applications`   | List applications for a job (by score)   |

## Scoring System

The API supports four question types, each with its own scoring logic:

| Type              | Scoring Rule                                         |
|-------------------|------------------------------------------------------|
| `single_choice`   | Full points if answer matches exactly                |
| `multi_choice`    | Partial credit based on overlap with correct options |
| `number`          | Full points if value falls within min/max range      |
| `text`            | Partial credit based on keyword matches              |

Final score is normalized to a 0-100 percentage.

## Design Decisions

- **JSON scoring rules** &mdash; employers provide only the fields relevant to their question type, avoiding wasted columns
- **Enum for question types** &mdash; compile-time safety instead of stringly-typed comparisons
- **Pydantic BaseSettings** &mdash; typed configuration with automatic .env loading
- **Dependency injection** &mdash; `get_or_404` helper eliminates repeated query-and-check boilerplate
- **Isolated test database** &mdash; tests run against a separate SQLite file, torn down after each test
- **SQLite for development** &mdash; zero setup required; swap `DATABASE_URL` for PostgreSQL in production
