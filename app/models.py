from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    position = Column(String(100), nullable=False, index=True)
    source = Column(String(50), nullable=True, default="Direct")
    current_stage = Column(String(30), nullable=False, default="Applied", index=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    history = relationship(
        "CandidateStageHistory",
        back_populates="candidate",
        cascade="all, delete-orphan",
        order_by="CandidateStageHistory.changed_at.asc()"
    )


class CandidateStageHistory(Base):
    __tablename__ = "candidate_stage_history"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    from_stage = Column(String(30), nullable=True)
    to_stage = Column(String(30), nullable=False)
    changed_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    changed_by = Column(String(100), nullable=False, default="system")
    reason = Column(String(255), nullable=True)

    candidate = relationship("Candidate", back_populates="history")


Index("idx_candidate_stage_age", Candidate.current_stage, Candidate.updated_at)