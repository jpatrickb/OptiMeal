"""
Pydantic schemas for API request/response validation.
"""

from .auth import UserCreate, UserLogin, Token, UserResponse
from .base import MessageResponse, ErrorResponse, PaginatedResponse, HealthResponse
from .food_item import FoodItemCreate, FoodItemUpdate, FoodItemResponse
from .pantry_item import PantryItemCreate, PantryItemUpdate, PantryItemResponse, PantryItemWithFoodResponse

__all__ = [
    # Auth schemas
    "UserCreate",
    "UserLogin",
    "Token",
    "UserResponse",
    # Base schemas
    "MessageResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "HealthResponse",
    # Food item schemas
    "FoodItemCreate",
    "FoodItemUpdate",
    "FoodItemResponse",
    # Pantry item schemas
    "PantryItemCreate",
    "PantryItemUpdate",
    "PantryItemResponse",
    "PantryItemWithFoodResponse",
]
