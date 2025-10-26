"""
Pydantic schemas for MealLog API endpoints.

Defines request/response models for meal logging functionality,
including computed nutrition totals.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class LoggedItemCreate(BaseModel):
    """Schema for creating a logged item within a meal."""
    food_item_id: UUID = Field(..., description="ID of the food item consumed")
    servings: Decimal = Field(..., gt=0, description="Number of servings consumed", decimal_places=2)


class LoggedItemResponse(BaseModel):
    """Schema for logged item in responses."""
    id: UUID
    food_item_id: UUID
    servings: Decimal
    food_item_name: str
    food_item_brand: Optional[str] = None
    total_calories: Optional[Decimal] = None
    total_protein_g: Optional[Decimal] = None
    total_carbs_g: Optional[Decimal] = None
    total_fat_g: Optional[Decimal] = None
    total_cost: Optional[Decimal] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MealLogCreate(BaseModel):
    """Schema for creating a meal log."""
    meal_name: Optional[str] = Field(None, max_length=255, description="Optional meal name")
    meal_type: Optional[str] = Field(None, description="Type of meal")
    logged_at: datetime = Field(..., description="When the meal was eaten")
    notes: Optional[str] = Field(None, description="Optional notes about the meal")
    items: List[LoggedItemCreate] = Field(..., min_items=1, description="Food items consumed in this meal")

    @validator('meal_type')
    def validate_meal_type(cls, v):
        """Validate meal_type is one of the allowed values."""
        if v is not None:
            allowed_types = {'breakfast', 'lunch', 'dinner', 'snack'}
            if v not in allowed_types:
                raise ValueError(f"meal_type must be one of {allowed_types}")
        return v

    @validator('logged_at')
    def validate_logged_at(cls, v):
        """Validate logged_at is not in the future."""
        if v and v > datetime.now(v.tzinfo):
            raise ValueError("logged_at cannot be in the future")
        return v

    @validator('items')
    def validate_items_not_empty(cls, v):
        """Validate that items list is not empty."""
        if not v:
            raise ValueError("At least one food item must be logged")
        return v


class MealLogUpdate(BaseModel):
    """Schema for updating a meal log."""
    meal_name: Optional[str] = Field(None, max_length=255)
    meal_type: Optional[str] = None
    notes: Optional[str] = None

    @validator('meal_type')
    def validate_meal_type(cls, v):
        """Validate meal_type is one of the allowed values."""
        if v is not None:
            allowed_types = {'breakfast', 'lunch', 'dinner', 'snack'}
            if v not in allowed_types:
                raise ValueError(f"meal_type must be one of {allowed_types}")
        return v


class NutritionTotals(BaseModel):
    """Computed nutrition totals for a meal."""
    total_calories: Optional[Decimal] = None
    total_protein_g: Optional[Decimal] = None
    total_carbs_g: Optional[Decimal] = None
    total_fat_g: Optional[Decimal] = None
    total_cost: Optional[Decimal] = None


class MealLogResponse(BaseModel):
    """Schema for meal log in responses with computed nutrition totals."""
    id: UUID
    user_id: UUID
    meal_name: Optional[str] = None
    meal_type: Optional[str] = None
    logged_at: datetime
    notes: Optional[str] = None
    logged_items: List[LoggedItemResponse] = []
    nutrition_totals: NutritionTotals
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MealLogListResponse(BaseModel):
    """Schema for paginated meal log list responses."""
    meals: List[MealLogResponse]
    total: int
    page: int
    per_page: int
    pages: int


class MealLogWarning(BaseModel):
    """Schema for warnings when logging meals (e.g., insufficient pantry)."""
    food_item_id: UUID
    food_item_name: str
    requested_servings: Decimal
    available_servings: Decimal
    message: str


class MealLogCreateResponse(BaseModel):
    """Schema for meal log creation response with warnings."""
    meal_log: MealLogResponse
    warnings: List[MealLogWarning] = []