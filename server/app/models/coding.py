from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class CodingProblem(Base, TimestampMixin):
    __tablename__ = "coding_problems"

    problem_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    input_format: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    output_format: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    constraints: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="coding_problems")
    test_cases: Mapped[List["CodingTestCase"]] = relationship(
        "CodingTestCase", back_populates="problem", cascade="all, delete-orphan"
    )
    submissions: Mapped[List["CodingSubmission"]] = relationship(
        "CodingSubmission", back_populates="problem", cascade="all, delete-orphan"
    )


class CodingTestCase(Base):
    __tablename__ = "coding_test_cases"

    test_case_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    problem_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("coding_problems.problem_id", ondelete="CASCADE"), nullable=False
    )
    input_data: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    marks: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    problem: Mapped["CodingProblem"] = relationship("CodingProblem", back_populates="test_cases")


class CodingSubmission(Base):
    __tablename__ = "coding_submissions"

    submission_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    problem_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("coding_problems.problem_id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    language: Mapped[str] = mapped_column(String(32), nullable=False)
    source_code: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=False)
    test_cases_passed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_test_cases: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    problem: Mapped["CodingProblem"] = relationship("CodingProblem", back_populates="submissions")
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
