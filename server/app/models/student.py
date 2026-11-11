from typing import Optional, List
from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Skill(Base):
    __tablename__ = "skills"

    skill_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    # Relationships
    student_skills: Mapped[List["StudentSkill"]] = relationship("StudentSkill", back_populates="skill")


class StudentSkill(Base):
    __tablename__ = "student_skills"

    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("student_profiles.user_id", ondelete="CASCADE"), primary_key=True
    )
    skill_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skills.skill_id", ondelete="CASCADE"), primary_key=True
    )
    proficiency: Mapped[str] = mapped_column(String(32), default="INTERMEDIATE", nullable=False)

    # Relationships
    student: Mapped["StudentProfile"] = relationship("StudentProfile", back_populates="skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="student_skills")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True
    )
    college_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("colleges.college_id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    github_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resume_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="student_profile")
    college: Mapped[Optional["College"]] = relationship("College", back_populates="students")
    skills: Mapped[List["StudentSkill"]] = relationship(
        "StudentSkill", back_populates="student", cascade="all, delete-orphan"
    )
