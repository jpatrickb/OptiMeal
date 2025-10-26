"""
Global exception handlers for consistent error responses.

Provides custom exception classes and handlers for FastAPI application.
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError


class OptiMealException(Exception):
    """Base exception for OptiMeal application."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundException(OptiMealException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class UnauthorizedException(OptiMealException):
    """Exception raised when user is not authorized."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(OptiMealException):
    """Exception raised when user does not have permission."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


async def optimeal_exception_handler(request: Request, exc: OptiMealException):
    """
    Handler for custom OptiMeal exceptions.

    Returns a consistent JSON error response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "type": type(exc).__name__
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handler for FastAPI HTTPException.

    Returns a consistent JSON error response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "type": "HTTPException"
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Handler for Pydantic validation errors.

    Returns a detailed JSON error response with validation errors.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "type": "ValidationError",
            "errors": exc.errors()
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handler for unexpected exceptions.

    Returns a generic error response and logs the exception.
    """
    # In production, log the exception here
    import traceback
    print(f"Unexpected error: {exc}")
    print(traceback.format_exc())

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "type": "InternalServerError"
        }
    )
