from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    achievement_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    student_achievements: Mapped[List["StudentAchievement"]] = relationship(
        "StudentAchievement", back_populates="achievement", cascade="all, delete-orphan"
    )


class StudentAchievement(Base):
    __tablename__ = "student_achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    achievement_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("achievements.achievement_id", ondelete="CASCADE"), nullable=False
    )
    event_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("events.event_id", ondelete="SET NULL"), nullable=True
    )
    certificate_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    awarded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    achievement: Mapped["Achievement"] = relationship("Achievement", back_populates="student_achievements")
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
    event: Mapped[Optional["Event"]] = relationship("Event", back_populates="student_achievements")
