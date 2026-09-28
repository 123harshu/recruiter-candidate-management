from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Candidate, CandidateStageHistory
from app.schemas import CandidateCreate, StageUpdatePayload
from app.services.stage_service import validate_stage_transition, StageTransitionError
from app.services.search_service import calculate_days_in_stage, apply_search_and_filters


def get_candidate_by_id(db: Session, candidate_id: int) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()


def get_candidate_by_email(db: Session, email: str) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.email == email).first()


def create_candidate(db: Session, candidate_in: CandidateCreate) -> Candidate:
    """Creates a candidate and automatically appends the initial stage history record."""
    now = datetime.now(timezone.utc)
    db_candidate = Candidate(
        full_name=candidate_in.full_name,
        email=candidate_in.email,
        phone=candidate_in.phone,
        position=candidate_in.position,
        source=candidate_in.source or "Direct",
        current_stage="Applied",
        created_at=now,
        updated_at=now
    )
    
    db.add(db_candidate)
    db.flush()  # Populates db_candidate.id

    # Create mandatory initial history entry
    initial_history = CandidateStageHistory(
        candidate_id=db_candidate.id,
        from_stage=None,
        to_stage="Applied",
        changed_at=now,
        changed_by="system",
        reason="Candidate created"
    )
    db.add(initial_history)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


def update_candidate_stage(
    db: Session,
    candidate_id: int,
    payload: StageUpdatePayload
) -> Candidate:
    """
    Atomic stage transition handler.
    Validates rules, updates candidate stage, and appends history.
    """
    candidate = get_candidate_by_id(db, candidate_id)
    if not candidate:
        raise ValueError(f"Candidate with ID {candidate_id} not found.")

    target_stage = payload.stage.strip().title()
    is_valid, msg = validate_stage_transition(candidate.current_stage, target_stage)
    if not is_valid:
        raise StageTransitionError(msg)

    now = datetime.now(timezone.utc)
    from_stage = candidate.current_stage

    try:
        # Atomic database transaction block
        candidate.current_stage = target_stage
        candidate.updated_at = now

        history_entry = CandidateStageHistory(
            candidate_id=candidate.id,
            from_stage=from_stage,
            to_stage=target_stage,
            changed_at=now,
            changed_by=payload.changed_by or "Recruiter",
            reason=payload.reason or "Stage updated"
        )
        db.add(history_entry)
        db.commit()
        db.refresh(candidate)
        return candidate
    except Exception as e:
        db.rollback()
        raise e


def search_candidates(
    db: Session,
    search: Optional[str] = None,
    stage: Optional[str] = None,
    min_days: Optional[int] = None,
    max_days: Optional[int] = None
) -> List[Candidate]:
    """Fetches candidate records and filters them through SearchService."""
    all_candidates = db.query(Candidate).all()
    return apply_search_and_filters(
        candidates=all_candidates,
        search_query=search,
        stage_filter=stage,
        min_days=min_days,
        max_days=max_days
    )


def build_candidate_schema_dict(candidate: Candidate) -> dict:
    """Helper to attach computed field `days_in_current_stage`."""
    return {
        "id": candidate.id,
        "full_name": candidate.full_name,
        "email": candidate.email,
        "phone": candidate.phone,
        "position": candidate.position,
        "source": candidate.source,
        "current_stage": candidate.current_stage,
        "created_at": candidate.created_at,
        "updated_at": candidate.updated_at,
        "days_in_current_stage": calculate_days_in_stage(candidate.updated_at),
        "history": candidate.history
    }