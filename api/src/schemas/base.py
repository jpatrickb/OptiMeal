"""
Base Pydantic schemas for common response patterns.

Provides reusable base schemas for API responses.
"""

from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """Simple message response schema."""

    message: str = Field(..., description="Response message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"message": "Operation completed successfully"}
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": "Resource not found",
                    "type": "ResourceNotFoundException"
                }
            ]
        }
    }


# Generic type for paginated results
T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""

    items: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [],
                    "total": 100,
                    "page": 1,
                    "page_size": 20,
                    "total_pages": 5
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(default="healthy", description="Service health status")
    version: str = Field(default="1.0.0", description="API version")
    timestamp: Optional[str] = Field(None, description="Current timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "version": "1.0.0",
                    "timestamp": "2025-10-26T00:00:00Z"
                }
            ]
        }
    }
