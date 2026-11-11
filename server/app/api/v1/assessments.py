from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.user import User
from app.models.assessment import Assessment, Question, QuestionOption
from app.schemas.assessment import (
    QuestionCreate,
    QuestionResponse,
    OptionResponse,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
)
from app.schemas.common import APIResponse
from app.api.deps import get_current_user, require_role, require_verified_organizer
from app.services.assessment_evaluator import evaluate_mcq_assessment

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.get("/{assessment_id}/questions", response_model=APIResponse[List[QuestionResponse]])
async def get_assessment_questions(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Question)
        .where(Question.assessment_id == assessment_id)
        .options(selectinload(Question.options))
    )
    result = await db.execute(stmt)
    questions = result.scalars().all()

    is_student = current_user.role == "student"

    items = []
    for q in questions:
        opt_list = []
        for opt in q.options:
            opt_list.append(
                OptionResponse(
                    option_id=opt.option_id,
                    option_text=opt.option_text,
                    # Conceal correct answer from students taking test
                    is_correct=None if is_student else opt.is_correct,
                )
            )
        items.append(
            QuestionResponse(
                question_id=q.question_id,
                assessment_id=q.assessment_id,
                question_text=q.question_text,
                question_type=q.question_type,
                marks=q.marks,
                negative_marks=q.negative_marks,
                options=opt_list,
            )
        )

    return APIResponse(data=items)


@router.post("/{assessment_id}/questions", response_model=APIResponse[dict], status_code=status.HTTP_201_CREATED)
async def add_question(
    assessment_id: int,
    req: QuestionCreate,
    current_user: User = Depends(require_verified_organizer),
    db: AsyncSession = Depends(get_db),
):
    question = Question(
        assessment_id=assessment_id,
        question_text=req.question_text,
        question_type=req.question_type,
        marks=req.marks,
        negative_marks=req.negative_marks,
    )
    db.add(question)
    await db.flush()

    for opt in req.options:
        option_record = QuestionOption(
            question_id=question.question_id,
            option_text=opt.option_text,
            is_correct=opt.is_correct,
        )
        db.add(option_record)

    await db.commit()
    await db.refresh(question)

    return APIResponse(message="Question created successfully", data={"question_id": question.question_id})


@router.post("/{assessment_id}/submit", response_model=APIResponse[AssessmentResultResponse])
async def submit_assessment(
    assessment_id: int,
    req: AssessmentSubmitRequest,
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    eval_result = await evaluate_mcq_assessment(
        assessment_id=assessment_id,
        student_id=current_user.user_id,
        submissions=req.submissions,
        db=db,
    )
    return APIResponse(
        message="Assessment evaluated successfully",
        data=AssessmentResultResponse(
            result_id=eval_result["result_id"],
            assessment_id=assessment_id,
            student_id=current_user.user_id,
            score=eval_result["score"],
            total_marks=eval_result["total_marks"],
            percentage=eval_result["percentage"],
            passed=eval_result["passed"],
        ),
    )
