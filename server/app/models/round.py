from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class RoundType(str, enum.Enum):
    APTITUDE = "APTITUDE"
    MCQ = "MCQ"
    CODING = "CODING"
    INTERVIEW = "INTERVIEW"


class RoundStatus(str, enum.Enum):
    UPCOMING = "UPCOMING"
    LIVE = "LIVE"
    EVALUATING = "EVALUATING"
    COMPLETED = "COMPLETED"


class EventRound(Base, TimestampMixin):
    __tablename__ = "event_rounds"

    round_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False
    )
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    round_type: Mapped[RoundType] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    total_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    passing_marks: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    status: Mapped[RoundStatus] = mapped_column(String(50), default=RoundStatus.UPCOMING, nullable=False)

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="rounds")
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment", back_populates="round", cascade="all, delete-orphan"
    )
    shortlists: Mapped[List["RoundShortlist"]] = relationship(
        "RoundShortlist", back_populates="round", cascade="all, delete-orphan"
    )
    interviews: Mapped[List["Interview"]] = relationship(
        "Interview", back_populates="round", cascade="all, delete-orphan"
    )
    assessment_results: Mapped[List["AssessmentResult"]] = relationship("AssessmentResult", back_populates="round")


class RoundShortlist(Base):
    __tablename__ = "round_shortlists"

    shortlist_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    round_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event_rounds.round_id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="SHORTLISTED", nullable=False)
    selected_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True)
    selected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    remarks: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    round: Mapped["EventRound"] = relationship("EventRound", back_populates="shortlists")
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
    selector: Mapped[Optional["User"]] = relationship("User", foreign_keys=[selected_by])


class EventResult(Base):
    __tablename__ = "event_results"

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="event_results")
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
