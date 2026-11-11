from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Hiring(Base, TimestampMixin):
    __tablename__ = "hiring"

    hiring_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False
    )
    event_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("events.event_id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(50), default="OFFERED", nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    job_type: Mapped[str] = mapped_column(String(50), default="FULL_TIME", nullable=False)
    offered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    rejected_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
    organization: Mapped["Organization"] = relationship("Organization", back_populates="hirings")
    event: Mapped[Optional["Event"]] = relationship("Event", back_populates="hirings")
