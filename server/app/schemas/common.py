from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = "Success"
    data: Optional[T] = None


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    limit: int
    items: list[T]
