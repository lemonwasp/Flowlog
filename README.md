# Flowlog

[![Tests](https://github.com/lemonwasp/Flowlog/actions/workflows/tests.yml/badge.svg)](https://github.com/lemonwasp/Flowlog/actions/workflows/tests.yml)

> A self-quantification project for exploring how activities, emotions, time spent, and satisfaction relate to personal flow.

Formerly **MyFace Tracker**, this project started as a personal experiment around a simple question:

> **What kinds of activities make me enter a state of deep focus, and how does that relate to how I feel afterward?**

## What this project tracks

- **Activities** — what was done and for how long
- **Emotions** — selected emotions or free-text emotional notes
- **Flow signals** — time spent and subjective satisfaction
- **Patterns over time** — relationships between activity, emotion, and perceived immersion

The backend models users, emotions, activity types, activity records, and flow-curve data. Free-text emotion input is also processed into an emotion label, score, and keywords.

## Stack

- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL / Supabase, with SQLite available for local development and isolated tests
- **Frontend:** HTML / CSS / JavaScript
- **Language:** Python
- **Tests:** pytest + FastAPI TestClient
- **CI:** GitHub Actions

## Architecture

The current backend is intentionally small and direct:

```text
Frontend / API client
        |
        v
FastAPI routes (backend/main.py)
        |
        +--> free-text emotion processing
        |    (backend/utils/emotion_processing.py)
        |
        v
CRUD functions (backend/crud.py)
        |
        v
SQLAlchemy models / sessions
        |
        v
SQLite or PostgreSQL / Supabase
```

FastAPI routes validate request data and obtain a database session through dependency injection. CRUD persistence operations are kept in `backend/crud.py`; `backend/main.py` provides the request-scoped database session, while SQLAlchemy models define the persisted entities. Free-text emotion records pass through the current emotion-processing helper before they are stored.

## Current status

Flowlog is an earlier learning project that has been stabilized and reframed around its original purpose: **understanding personal flow through recorded behavior and subjective state**.

The current repository foundation includes explicit environment configuration, separated runtime/development dependencies, repeatable pytest coverage, isolated API integration tests, a manual end-to-end smoke test, and CI on pull requests and pushes to `main`.

## Local setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it with the command appropriate for your shell.

### 2. Configure the environment

Copy the checked-in example file:

```bash
cp .env.example .env
```

The default example uses a local SQLite database:

```env
DATABASE_URL=sqlite:///./flowlog.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500
```

Use a PostgreSQL/Supabase connection string instead when running against that environment. Keep real credentials in `.env`; the file is ignored by Git.

### 3. Install dependencies

For normal application runtime:

```bash
python -m pip install -r requirements.txt
```

For development and tests:

```bash
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` includes the runtime dependencies plus the test-only packages.

### 4. Start the API

```bash
uvicorn backend.main:app --reload
```

Then open `frontend/index.html` in a browser to inspect the current frontend.

## Tests

Run the repeatable automated test suite with:

```bash
python -m pytest
```

The suite includes unit/schema coverage and isolated API integration tests. Integration tests use an in-memory SQLite database so they do not require a live Supabase/PostgreSQL instance.

GitHub Actions runs the same pytest suite on pull requests and pushes to `main`.

## Manual smoke test

For a running API backed by a reachable database, run:

```bash
python scripts/smoke_test_api.py
```

This is intentionally separate from pytest because it exercises a live API/database path and creates application data. Each run uses unique smoke-test values, applies request timeouts, rejects redirects and non-2xx responses, and avoids logging full response bodies.

## Current limitations

This repository is a stabilized learning project, not a production-ready service. Important current limitations include:

- Database tables are created with `Base.metadata.create_all()` when the application module loads; there is no migration tool such as Alembic yet.
- Free-text emotion processing is a simple keyword-based heuristic with whitespace tokenization, not a robust NLP or machine-learning model.
- The API is intentionally small and does not yet provide a complete production-style resource lifecycle, authentication, or authorization.
- The manual smoke test creates records in the configured database and does not clean them up afterward.
- The frontend is a simple static interface and there is no production deployment setup documented yet.

These boundaries are kept explicit so future improvements can be evaluated against the current implementation rather than implied as already complete.

## Direction

Possible future analysis includes:

- Which activities correlate with the highest satisfaction?
- Does longer time spent actually mean deeper flow?
- Which activities tend to improve or worsen emotional state?
- Are there recurring combinations of activity, emotion, and satisfaction that predict a strong flow state?

---

**Flowlog is not intended to be a generic productivity tracker.** Its focus is the relationship between behavior, emotion, and the subjective experience of immersion.
