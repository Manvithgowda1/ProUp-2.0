from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.students import router as students_router
from app.api.v1.events import router as events_router
from app.api.v1.assessments import router as assessments_router
from app.api.v1.coding import router as coding_router
from app.api.v1.hiring import router as hiring_router
from app.api.v1.admin import router as admin_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(students_router)
api_router.include_router(events_router)
api_router.include_router(assessments_router)
api_router.include_router(coding_router)
api_router.include_router(hiring_router)
api_router.include_router(admin_router)
