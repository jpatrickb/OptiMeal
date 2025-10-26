"""
Pydantic schemas for Recipe API endpoints.

Defines request/response models for recipe functionality,
including creation from meal logs and ingredient lists.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class RecipeIngredientCreate(BaseModel):
    """Schema for creating a recipe ingredient."""
    food_item_id: UUID = Field(..., description="ID of the food item")
    servings: Decimal = Field(..., gt=0, description="Number of servings in recipe", decimal_places=2)

    @validator('servings')
    def validate_servings(cls, v):
        """Validate servings is greater than 0."""
        if v <= 0:
            raise ValueError("servings must be greater than 0")
        return v


class RecipeIngredientResponse(BaseModel):
    """Schema for recipe ingredient in responses."""
    id: UUID
    recipe_id: UUID
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


class RecipeCreate(BaseModel):
    """Schema for creating a recipe."""
    name: str = Field(..., max_length=255, description="Recipe name")
    description: Optional[str] = Field(None, description="Optional description/instructions")
    ingredients: Optional[List[RecipeIngredientCreate]] = Field(None, description="Recipe ingredients")

    @validator('name')
    def validate_name(cls, v):
        """Validate name is not empty."""
        if not v or not v.strip():
            raise ValueError("Recipe name cannot be empty")
        return v.strip()

    @validator('ingredients')
    def validate_ingredients(cls, v):
        """Validate ingredients if provided."""
        if v is not None and len(v) == 0:
            raise ValueError("If ingredients are provided, at least one ingredient is required")
        return v


class RecipeCreateFromMealLog(BaseModel):
    """Schema for creating a recipe from a meal log."""
    name: str = Field(..., max_length=255, description="Recipe name")
    description: Optional[str] = Field(None, description="Optional description/instructions")
    meal_log_id: UUID = Field(..., description="ID of the meal log to copy from")

    @validator('name')
    def validate_name(cls, v):
        """Validate name is not empty."""
        if not v or not v.strip():
            raise ValueError("Recipe name cannot be empty")
        return v.strip()


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe."""
    name: Optional[str] = Field(None, max_length=255, description="Recipe name")
    description: Optional[str] = Field(None, description="Optional description/instructions")

    @validator('name')
    def validate_name(cls, v):
        """Validate name is not empty if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Recipe name cannot be empty")
        return v.strip() if v else None


class RecipeNutritionTotals(BaseModel):
    """Computed nutrition totals for a recipe."""
    total_calories: Optional[Decimal] = None
    total_protein_g: Optional[Decimal] = None
    total_carbs_g: Optional[Decimal] = None
    total_fat_g: Optional[Decimal] = None
    total_cost: Optional[Decimal] = None


class RecipeResponse(BaseModel):
    """Schema for recipe in responses with ingredients list."""
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    created_from_meal_log_id: Optional[UUID] = None
    ingredients: List[RecipeIngredientResponse] = []
    nutrition_totals: RecipeNutritionTotals
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeListItem(BaseModel):
    """Schema for recipe in list responses (without full ingredient details)."""
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    ingredient_count: int
    nutrition_totals: RecipeNutritionTotals
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    """Schema for paginated recipe list responses."""
    recipes: List[RecipeListItem]
    total: int
    page: int
    per_page: int
    pages: int