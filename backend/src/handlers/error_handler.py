from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union
from ..utils.logging import get_logger
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

logger = get_logger("error-handler")

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions globally.

    Args:
        request: The incoming request
        exc: The HTTP exception that occurred

    Returns:
        JSONResponse with error details
    """
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail} for {request.url}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP_ERROR",
            "message": exc.detail,
            "path": str(request.url),
            "status_code": exc.status_code
        }
    )

async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handle validation exceptions globally.

    Args:
        request: The incoming request
        exc: The validation exception that occurred

    Returns:
        JSONResponse with error details
    """
    logger.error(f"Validation Error: {str(exc)} for {request.url}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": exc.errors(),
            "path": str(request.url)
        }
    )

async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    Handle database exceptions globally.

    Args:
        request: The incoming request
        exc: The database exception that occurred

    Returns:
        JSONResponse with error details
    """
    logger.error(f"Database Error: {str(exc)} for {request.url}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "DATABASE_ERROR",
            "message": "A database error occurred",
            "path": str(request.url)
        }
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions globally.

    Args:
        request: The incoming request
        exc: The general exception that occurred

    Returns:
        JSONResponse with error details
    """
    logger.error(f"General Error: {str(exc)} for {request.url}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_ERROR",
            "message": "An internal error occurred",
            "path": str(request.url)
        }
    )

def register_error_handlers(app):
    """
    Register all error handlers with the FastAPI app.

    Args:
        app: The FastAPI application instance
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    logger.info("Error handlers registered with the application")