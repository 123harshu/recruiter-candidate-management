"""High-level candidate service orchestrator for route handlers."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app import crud
from app.schemas import CandidateCreate, StageUpdatePayload


def create_new_candidate(db: Session, payload: CandidateCreate) -> Dict[str, Any]:
    existing = crud.get_candidate_by_email(db, payload.email)
    if existing:
        raise ValueError(f"Candidate with email '{payload.email}' already exists.")
    
    candidate = crud.create_candidate(db, payload)
    return crud.build_candidate_schema_dict(candidate)


def update_stage(db: Session, candidate_id: int, payload: StageUpdatePayload) -> Dict[str, Any]:
    candidate = crud.update_candidate_stage(db, candidate_id, payload)
    return crud.build_candidate_schema_dict(candidate)


def get_candidate(db: Session, candidate_id: int) -> Optional[Dict[str, Any]]:
    candidate = crud.get_candidate_by_id(db, candidate_id)
    if not candidate:
        return None
    return crud.build_candidate_schema_dict(candidate)


def query_candidates(
    db: Session,
    search: Optional[str] = None,
    stage: Optional[str] = None,
    min_days: Optional[int] = None,
    max_days: Optional[int] = None
) -> List[Dict[str, Any]]:
    candidates = crud.search_candidates(db, search, stage, min_days, max_days)
    return [crud.build_candidate_schema_dict(c) for c in candidates]