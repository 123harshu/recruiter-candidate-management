from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


class StageHistoryBase(BaseModel):
    from_stage: Optional[str] = None
    to_stage: str
    changed_by: str = "system"
    reason: Optional[str] = None


class StageHistoryResponse(StageHistoryBase):
    id: int
    candidate_id: int
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    position: str
    source: Optional[str] = "Direct"


class CandidateCreate(CandidateBase):
    pass


class StageUpdatePayload(BaseModel):
    stage: str
    changed_by: Optional[str] = "Recruiter"
    reason: Optional[str] = "Stage updated"


class CandidateResponse(CandidateBase):
    id: int
    current_stage: str
    created_at: datetime
    updated_at: datetime
    days_in_current_stage: int
    history: List[StageHistoryResponse] = []

    model_config = ConfigDict(from_attributes=True)


class CandidateListResponse(BaseModel):
    total: int
    candidates: List[CandidateResponse]