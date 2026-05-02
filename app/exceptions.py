from fastapi import HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

class ErrorResponse(BaseModel):
    status_code: int
    message: str
    error_type: str
    details: Optional[Dict[str, Any]] = None

class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = "Custom exception A occurred"):
        super().__init__(status_code=400, detail=detail)

class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)

class ValidationErrorResponse(BaseModel):
    status_code: int = 422
    message: str = "Validation error"
    errors: list