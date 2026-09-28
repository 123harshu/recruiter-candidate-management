# AI-Assisted Development Decision Log

*Note: This log records key engineering decisions and choices made during AI-assisted development.*

---

### Decision 1: Framework Choice — FastAPI
* **AI Suggestion:** Use FastAPI due to speed, automatic OpenAPI/Swagger documentation generation, and native integration with Pydantic v2.
* **Developer Decision:** Accepted. FastAPI delivers clean REST API contracts and clear verification endpoints out of the box without boilerplate.

---

### Decision 2: Database Layer — SQLite + SQLAlchemy
* **AI Suggestion:** PostgreSQL is standard for production apps, but SQLite with SQLAlchemy ORM offers zero-friction execution on Windows without external database server installation.
* **Developer Decision:** Accepted. SQLite ensures `setup.bat` runs immediately on any Windows machine while maintaining a modular database layer that can be migrated to PostgreSQL later.

---

### Decision 3: Search Engine — RapidFuzz
* **AI Suggestion:** Implement `rapidfuzz.process.extract` with `partial_ratio` scoring to allow recruiters to match misspelled or incomplete names.
* **Developer Decision:** Accepted with a similarity threshold of `60.0` to avoid over-broad matching.

---

### Decision 4: Immutable Audit Trail Enforcement
* **AI Suggestion:** Enforce stage history appends in the backend service layer via database transactions instead of reliance on database triggers.
* **Developer Decision:** Implemented atomic transaction blocks inside `crud.update_candidate_stage()` to guarantee that candidate stage updates and history insertions fail or succeed together.