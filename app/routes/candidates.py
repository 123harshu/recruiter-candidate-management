from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    CandidateCreate,
    CandidateResponse,
    StageUpdatePayload,
    StageHistoryResponse
)
from app.services import candidate_service
from app.services.stage_service import StageTransitionError

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])


@router.get("", response_model=List[CandidateResponse])
def list_candidates(
    search: Optional[str] = Query(None, description="Fuzzy match on candidate name"),
    stage: Optional[str] = Query(None, description="Filter by stage name"),
    min_days_in_stage: Optional[int] = Query(None, description="Minimum days spent in stage"),
    max_days_in_stage: Optional[int] = Query(None, description="Maximum days spent in stage"),
    db: Session = Depends(get_db)
):
    """Retrieve filtered candidate records."""
    return candidate_service.query_candidates(
        db, search=search, stage=stage, min_days=min_days_in_stage, max_days=max_days_in_stage
    )


@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
def create_candidate(payload: CandidateCreate, db: Session = Depends(get_db)):
    """Create new candidate starting in 'Applied' stage."""
    try:
        return candidate_service.create_new_candidate(db, payload)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate_details(candidate_id: int, db: Session = Depends(get_db)):
    """Retrieve candidate details by ID."""
    candidate = candidate_service.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found.")
    return candidate


@router.patch("/{candidate_id}/stage", response_model=CandidateResponse)
def transition_candidate_stage(
    candidate_id: int,
    payload: StageUpdatePayload,
    db: Session = Depends(get_db)
):
    """Transitions a candidate stage atomically with audit history logging."""
    try:
        return candidate_service.update_stage(db, candidate_id, payload)
    except StageTransitionError as err:
        raise HTTPException(status_code=400, detail={"success": False, "message": str(err)})
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/{candidate_id}/history", response_model=List[StageHistoryResponse])
def get_candidate_history(candidate_id: int, db: Session = Depends(get_db)):
    """Retrieve append-only candidate stage history audit trail."""
    candidate = candidate_service.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found.")
    return candidate["history"]