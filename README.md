# Flowlog

> A self-quantification project for exploring how activities, emotions, time spent, and satisfaction relate to personal flow.

Formerly **MyFace Tracker**, this project started as a personal experiment around a simple question:

> **What kinds of activities make me enter a state of deep focus, and how does that relate to how I feel afterward?**

## What this project tracks

- **Activities** — what was done and for how long
- **Emotions** — selected emotions or free-text emotional notes
- **Flow signals** — time spent and subjective satisfaction
- **Patterns over time** — relationships between activity, emotion, and perceived immersion

The backend already models users, emotions, activity types, activity records, and flow-curve data. Free-text emotion input is also processed into an emotion label, score, and keywords.

## Current stack

- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL / Supabase
- **Frontend:** HTML / CSS / JavaScript
- **Language:** Python

## Current status

This is an earlier learning project that is being cleaned up and reframed around its original purpose: **understanding personal flow through recorded behavior and subjective state**.

Before expanding the product further, the current focus is on stabilizing configuration, dependencies, tests, and repository structure so that the implementation can be reproduced reliably.

## Running the current version

1. Configure the database connection through the `DATABASE_URL` environment variable.
2. Start the FastAPI server:

   ```bash
   uvicorn backend.main:app --reload
   ```

3. Open `frontend/index.html` in a browser to inspect the current frontend.

## Direction

Possible future analysis includes:

- Which activities correlate with the highest satisfaction?
- Does longer time spent actually mean deeper flow?
- Which activities tend to improve or worsen emotional state?
- Are there recurring combinations of activity, emotion, and satisfaction that predict a strong flow state?

---

**Flowlog is not intended to be a generic productivity tracker.** Its focus is the relationship between behavior, emotion, and the subjective experience of immersion.
