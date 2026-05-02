from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import List
from app.exceptions import CustomExceptionA, CustomExceptionB

class ErrorDetail(BaseModel):
    field: str | None = None
    message: str

class ErrorResponse(BaseModel):
    error_code: int
    message: str
    details: List[ErrorDetail] | None = None

async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=exc.status_code,
            message=exc.detail,
            details=[ErrorDetail(field="price", message="Price must be greater than 0")]
        ).model_dump()
    )

async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=exc.status_code,
            message=exc.detail
        ).model_dump()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        details.append(ErrorDetail(field=field, message=error["msg"]))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error_code=422,
            message="Validation error",
            details=details
        ).model_dump()
    )
