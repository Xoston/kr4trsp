from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import products, users
from app.exceptions import (
    CustomExceptionA,
    CustomExceptionB,
    ErrorResponse,
    ValidationErrorResponse,
)

app = FastAPI(
    title="Контрольная работа №4 API",
    description="FastAPI приложение с миграциями Alembic и тестами",
    version="1.0.0",
)

# Обработчик CustomExceptionA
@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    error_response = ErrorResponse(
        status_code=exc.status_code,
        message=exc.detail,
        error_type="CustomExceptionA",
    )
    return JSONResponse(status_code=exc.status_code, content=error_response.model_dump())

# Обработчик CustomExceptionB
@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    error_response = ErrorResponse(
        status_code=exc.status_code,
        message=exc.detail,
        error_type="CustomExceptionB",
    )
    return JSONResponse(status_code=exc.status_code, content=error_response.model_dump())

# Обработчик ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )
    error_response = ValidationErrorResponse(
        status_code=422,
        message="Validation error",
        errors=errors,
    )
    return JSONResponse(status_code=422, content=error_response.model_dump())

# Подключаем роутеры
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "message": "Контрольная работа №4 API",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}