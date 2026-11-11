from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    organization_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cin: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    organizers: Mapped[List["OrganizerProfile"]] = relationship("OrganizerProfile", back_populates="organization")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="organization")
    hirings: Mapped[List["Hiring"]] = relationship("Hiring", back_populates="organization")


class College(Base):
    __tablename__ = "colleges"

    college_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    students: Mapped[List["StudentProfile"]] = relationship("StudentProfile", back_populates="college")
