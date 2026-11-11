from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.auth import (
    Token,
    TokenPayload,
    LoginRequest,
    RefreshTokenRequest,
    StudentRegisterRequest,
    OrganizerRegisterRequest,
    UserSummary,
)
from app.schemas.student import (
    SkillResponse,
    StudentSkillResponse,
    AddSkillRequest,
    CollegeResponse,
    StudentProfileUpdate,
    StudentProfileResponse,
)
from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventRecommendation,
)
from app.schemas.round import (
    RoundCreate,
    RoundResponse,
    ShortlistCreate,
    ShortlistResponse,
)
from app.schemas.assessment import (
    QuestionCreate,
    QuestionResponse,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
)
from app.schemas.coding import (
    TestCaseCreate,
    TestCaseResponse,
    CodingProblemCreate,
    CodingProblemResponse,
    CodeSubmissionRequest,
    CodeSubmissionResponse,
)
from app.schemas.hiring import OfferCreate, OfferRespond, OfferResponse
from app.schemas.admin import (
    OrganizerVerifyRequest,
    EventModerateRequest,
    PlatformAnalyticsResponse,
)
