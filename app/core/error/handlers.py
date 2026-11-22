import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.common.response import ApiResponse
from app.core.error.exceptions import AppException

log = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(_: Request, e: AppException):
        return JSONResponse(status_code=e.status_code, content=ApiResponse.fail(e.message, e.code).model_dump())

    @app.exception_handler(RequestValidationError)
    async def handle_validation(_: Request, e: RequestValidationError):
        content = ApiResponse.fail("요청 값이 올바르지 않아요.", "VALIDATION_ERROR").model_dump()
        content["errors"] = e.errors()
        return JSONResponse(status_code=422, content=content)

    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, e: Exception):
        log.exception("unhandled error")
        return JSONResponse(status_code=500, content=ApiResponse.fail("서버 오류가 발생했어요.", "INTERNAL_ERROR").model_dump())
