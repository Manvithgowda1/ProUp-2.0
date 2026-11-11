from typing import Optional, List
from pydantic import BaseModel, Field


class TestCaseCreate(BaseModel):
    input_data: str
    expected_output: str
    marks: float = 10.0
    is_hidden: bool = True


class TestCaseResponse(BaseModel):
    test_case_id: int
    problem_id: int
    input_data: str
    expected_output: Optional[str] = None
    marks: float
    is_hidden: bool

    class Config:
        from_attributes = True


class CodingProblemCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: str
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None
    difficulty: str = "MEDIUM"


class CodingProblemResponse(BaseModel):
    problem_id: int
    assessment_id: int
    title: str
    description: str
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None
    difficulty: str
    test_cases: List[TestCaseResponse] = []

    class Config:
        from_attributes = True


class CodeSubmissionRequest(BaseModel):
    language: str = Field(..., description="python, javascript, cpp, java")
    source_code: str


class CodeSubmissionResponse(BaseModel):
    submission_id: int
    problem_id: int
    language: str
    status: str
    test_cases_passed: int
    total_test_cases: int
    score: float

    class Config:
        from_attributes = True
