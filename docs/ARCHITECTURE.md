# Architecture Documentation

## System Architecture

```text
Browser / Client (Vanilla JS + Jinja2 Templates)
       │
       ▼
FastAPI Application (Uvicorn Server)
       │
       ├── Page Router / API Router
       │
       ├── Services Layer
       │     ├── CandidateService
       │     ├── StageService (Transition Validation)
       │     └── SearchService (RapidFuzz + Time Filters)
       │
       ▼
SQLAlchemy ORM
       │
       ▼
SQLite Database (`data/candidates.db`)