"""
Pydantic schemas for LoggedItem API endpoints.

Defines request/response models for individual logged items within meals.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class LoggedItemCreate(BaseModel):
    """Schema for creating a logged item."""
    meal_log_id: UUID = Field(..., description="ID of the meal log")
    food_item_id: UUID = Field(..., description="ID of the food item consumed")
    servings: Decimal = Field(..., gt=0, description="Number of servings consumed", decimal_places=2)

    @validator('servings')
    def validate_servings(cls, v):
        """Validate servings is greater than 0."""
        if v <= 0:
            raise ValueError("servings must be greater than 0")
        return v


class LoggedItemUpdate(BaseModel):
    """Schema for updating a logged item."""
    servings: Optional[Decimal] = Field(None, gt=0, description="Number of servings consumed", decimal_places=2)

    @validator('servings')
    def validate_servings(cls, v):
        """Validate servings is greater than 0."""
        if v is not None and v <= 0:
            raise ValueError("servings must be greater than 0")
        return v


class LoggedItemResponse(BaseModel):
    """Schema for logged item in responses."""
    id: UUID
    meal_log_id: UUID
    food_item_id: UUID
    servings: Decimal
    # Computed nutrition totals
    total_calories: Optional[Decimal] = None
    total_protein_g: Optional[Decimal] = None
    total_carbs_g: Optional[Decimal] = None
    total_fat_g: Optional[Decimal] = None
    total_cost: Optional[Decimal] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LoggedItemWithFoodDetails(BaseModel):
    """Schema for logged item with food details included."""
    id: UUID
    meal_log_id: UUID
    food_item_id: UUID
    servings: Decimal
    # Food item details
    food_item_name: str
    food_item_brand: Optional[str] = None
    food_item_serving_unit: str
    # Computed nutrition totals
    total_calories: Optional[Decimal] = None
    total_protein_g: Optional[Decimal] = None
    total_carbs_g: Optional[Decimal] = None
    total_fat_g: Optional[Decimal] = None
    total_cost: Optional[Decimal] = None
    created_at: datetime

    class Config:
        from_attributes = True