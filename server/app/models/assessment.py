from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Assessment(Base, TimestampMixin):
    __tablename__ = "assessments"

    assessment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    round_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event_rounds.round_id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    total_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    passing_marks: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)

    # Relationships
    round: Mapped["EventRound"] = relationship("EventRound", back_populates="assessments")
    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="assessment", cascade="all, delete-orphan"
    )
    answers: Mapped[List["Answer"]] = relationship("Answer", back_populates="assessment")
    coding_problems: Mapped[List["CodingProblem"]] = relationship(
        "CodingProblem", back_populates="assessment", cascade="all, delete-orphan"
    )
    assessment_results: Mapped[List["AssessmentResult"]] = relationship("AssessmentResult", back_populates="assessment")


class Question(Base):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(50), default="MCQ", nullable=False)
    marks: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    negative_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="questions")
    options: Mapped[List["QuestionOption"]] = relationship(
        "QuestionOption", back_populates="question", cascade="all, delete-orphan"
    )
    answers: Mapped[List["Answer"]] = relationship("Answer", back_populates="question")


class QuestionOption(Base):
    __tablename__ = "question_options"

    option_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.question_id", ondelete="CASCADE"), nullable=False
    )
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    question: Mapped["Question"] = relationship("Question", back_populates="options")
    selected_in_answers: Mapped[List["Answer"]] = relationship("Answer", back_populates="selected_option")


class Answer(Base):
    __tablename__ = "answers"
    __table_args__ = (UniqueConstraint("question_id", "student_id", name="uq_question_student_answer"),)

    answer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.question_id", ondelete="CASCADE"), nullable=False
    )
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    selected_option_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("question_options.option_id", ondelete="SET NULL"), nullable=True
    )
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    marks_obtained: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    question: Mapped["Question"] = relationship("Question", back_populates="answers")
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="answers")
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
    selected_option: Mapped[Optional["QuestionOption"]] = relationship(
        "QuestionOption", back_populates="selected_in_answers"
    )


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False
    )
    round_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event_rounds.round_id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="assessment_results")
    round: Mapped["EventRound"] = relationship("EventRound", back_populates="assessment_results")
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
