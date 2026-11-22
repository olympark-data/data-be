from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None
    code: str | None = None

    @classmethod
    def ok(cls, data: T | None = None) -> "ApiResponse[T]":
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, message: str, code: str | None = None) -> "ApiResponse[None]":
        return cls(success=False, message=message, code=code)


class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    size: int
    total: int
