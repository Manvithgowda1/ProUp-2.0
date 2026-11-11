from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Integer, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ORGANIZER = "organizer"
    ADMIN = "admin"


class VerificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(String(32), default=UserRole.STUDENT, nullable=False)

    # Relationships
    student_profile: Mapped[Optional["StudentProfile"]] = relationship(
        "StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    organizer_profile: Mapped[Optional["OrganizerProfile"]] = relationship(
        "OrganizerProfile",
        foreign_keys="OrganizerProfile.user_id",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user")
    blogs: Mapped[List["Blog"]] = relationship("Blog", back_populates="author")


class OrganizerProfile(Base):
    __tablename__ = "organizer_profiles"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True
    )
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.organization_id", ondelete="RESTRICT"), nullable=False
    )
    verification_status: Mapped[VerificationStatus] = mapped_column(
        String(32), default=VerificationStatus.PENDING, nullable=False
    )
    verified_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="organizer_profile")
    verifier: Mapped[Optional["User"]] = relationship("User", foreign_keys=[verified_by])
    organization: Mapped["Organization"] = relationship("Organization", back_populates="organizers")
