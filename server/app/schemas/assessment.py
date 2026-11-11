from typing import Optional, List
from pydantic import BaseModel, Field


class OptionInput(BaseModel):
    option_text: str
    is_correct: bool = False


class OptionResponse(BaseModel):
    option_id: int
    option_text: str
    is_correct: Optional[bool] = None

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    question_text: str
    question_type: str = "MCQ"
    marks: float = 1.0
    negative_marks: float = 0.0
    options: List[OptionInput]


class QuestionResponse(BaseModel):
    question_id: int
    assessment_id: int
    question_text: str
    question_type: str
    marks: float
    negative_marks: float
    options: List[OptionResponse] = []

    class Config:
        from_attributes = True


class SingleAnswerSubmission(BaseModel):
    question_id: int
    selected_option_id: int


class AssessmentSubmitRequest(BaseModel):
    submissions: List[SingleAnswerSubmission]


class AssessmentResultResponse(BaseModel):
    result_id: Optional[int] = None
    assessment_id: int
    student_id: int
    score: float
    total_marks: float
    percentage: float
    passed: bool
    rank: Optional[int] = None

    class Config:
        from_attributes = True
