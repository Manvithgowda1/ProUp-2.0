from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class EventStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    LIVE = "LIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class EventType(str, enum.Enum):
    HACKATHON = "HACKATHON"
    COMPETITION = "COMPETITION"
    WORKSHOP = "WORKSHOP"
    HIRING_CHALLENGE = "HIRING_CHALLENGE"


class EventMode(str, enum.Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    HYBRID = "HYBRID"


class RegistrationStatus(str, enum.Enum):
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"


class AttendanceStatus(str, enum.Enum):
    PENDING = "PENDING"
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False
    )
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    event_type: Mapped[EventType] = mapped_column(String(50), default=EventType.HIRING_CHALLENGE, nullable=False)
    event_mode: Mapped[EventMode] = mapped_column(String(50), default=EventMode.ONLINE, nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    registration_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[EventStatus] = mapped_column(String(50), default=EventStatus.DRAFT, nullable=False)

    approved_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="events")
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    approver: Mapped[Optional["User"]] = relationship("User", foreign_keys=[approved_by])
    registrations: Mapped[List["EventRegistration"]] = relationship(
        "EventRegistration", back_populates="event", cascade="all, delete-orphan"
    )
    rounds: Mapped[List["EventRound"]] = relationship(
        "EventRound", back_populates="event", cascade="all, delete-orphan", order_by="EventRound.round_number"
    )
    event_results: Mapped[List["EventResult"]] = relationship("EventResult", back_populates="event")
    student_achievements: Mapped[List["StudentAchievement"]] = relationship("StudentAchievement", back_populates="event")
    hirings: Mapped[List["Hiring"]] = relationship("Hiring", back_populates="event")


class EventRegistration(Base):
    __tablename__ = "event_registrations"
    __table_args__ = (UniqueConstraint("event_id", "student_id", name="uq_event_student_registration"),)

    registration_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[RegistrationStatus] = mapped_column(
        String(32), default=RegistrationStatus.REGISTERED, nullable=False
    )
    attendance_status: Mapped[AttendanceStatus] = mapped_column(
        String(32), default=AttendanceStatus.PENDING, nullable=False
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="registrations")
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
