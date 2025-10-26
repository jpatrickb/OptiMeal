"""
Pydantic schemas for FoodItem model.

Schemas for creating, updating, and retrieving food items with nutritional information.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class FoodItemBase(BaseModel):
    """Base schema for FoodItem with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Name of the food item")
    brand: Optional[str] = Field(None, max_length=255, description="Brand name (optional)")

    # Serving Information
    serving_size: Decimal = Field(..., gt=0, description="Size of one serving")
    serving_unit: str = Field(..., min_length=1, max_length=50, description="Unit of serving (e.g., 'cup', 'oz', 'g')")

    # Macronutrients (per serving)
    calories: Optional[Decimal] = Field(None, ge=0, description="Calories per serving")
    protein_g: Optional[Decimal] = Field(None, ge=0, description="Protein in grams")
    carbs_g: Optional[Decimal] = Field(None, ge=0, description="Carbohydrates in grams")
    fat_g: Optional[Decimal] = Field(None, ge=0, description="Total fat in grams")

    # Fat Breakdown
    saturated_fat_g: Optional[Decimal] = Field(None, ge=0, description="Saturated fat in grams")
    trans_fat_g: Optional[Decimal] = Field(None, ge=0, description="Trans fat in grams")
    cholesterol_mg: Optional[Decimal] = Field(None, ge=0, description="Cholesterol in milligrams")

    # Micronutrients
    sodium_mg: Optional[Decimal] = Field(None, ge=0, description="Sodium in milligrams")
    fiber_g: Optional[Decimal] = Field(None, ge=0, description="Dietary fiber in grams")
    sugar_g: Optional[Decimal] = Field(None, ge=0, description="Sugar in grams")
    vitamin_a_mcg: Optional[Decimal] = Field(None, ge=0, description="Vitamin A in micrograms")
    vitamin_c_mg: Optional[Decimal] = Field(None, ge=0, description="Vitamin C in milligrams")
    calcium_mg: Optional[Decimal] = Field(None, ge=0, description="Calcium in milligrams")
    iron_mg: Optional[Decimal] = Field(None, ge=0, description="Iron in milligrams")

    # Cost
    cost_per_serving: Optional[Decimal] = Field(None, ge=0, description="Cost in USD per serving")


class FoodItemCreate(FoodItemBase):
    """Schema for creating a new food item."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Whole Milk",
                    "brand": "Organic Valley",
                    "serving_size": 1.0,
                    "serving_unit": "cup",
                    "calories": 150,
                    "protein_g": 8,
                    "carbs_g": 12,
                    "fat_g": 8,
                    "saturated_fat_g": 5,
                    "trans_fat_g": 0,
                    "cholesterol_mg": 35,
                    "sodium_mg": 120,
                    "fiber_g": 0,
                    "sugar_g": 12,
                    "calcium_mg": 300,
                    "cost_per_serving": 0.50
                }
            ]
        }
    }


class FoodItemUpdate(BaseModel):
    """Schema for updating a food item (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    brand: Optional[str] = Field(None, max_length=255)
    serving_size: Optional[Decimal] = Field(None, gt=0)
    serving_unit: Optional[str] = Field(None, min_length=1, max_length=50)
    calories: Optional[Decimal] = Field(None, ge=0)
    protein_g: Optional[Decimal] = Field(None, ge=0)
    carbs_g: Optional[Decimal] = Field(None, ge=0)
    fat_g: Optional[Decimal] = Field(None, ge=0)
    saturated_fat_g: Optional[Decimal] = Field(None, ge=0)
    trans_fat_g: Optional[Decimal] = Field(None, ge=0)
    cholesterol_mg: Optional[Decimal] = Field(None, ge=0)
    sodium_mg: Optional[Decimal] = Field(None, ge=0)
    fiber_g: Optional[Decimal] = Field(None, ge=0)
    sugar_g: Optional[Decimal] = Field(None, ge=0)
    vitamin_a_mcg: Optional[Decimal] = Field(None, ge=0)
    vitamin_c_mg: Optional[Decimal] = Field(None, ge=0)
    calcium_mg: Optional[Decimal] = Field(None, ge=0)
    iron_mg: Optional[Decimal] = Field(None, ge=0)
    cost_per_serving: Optional[Decimal] = Field(None, ge=0)


class FoodItemResponse(FoodItemBase):
    """Schema for food item response with database fields."""

    id: UUID = Field(..., description="Unique food item identifier")
    user_id: UUID = Field(..., description="Owner of this food item")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "name": "Whole Milk",
                    "brand": "Organic Valley",
                    "serving_size": 1.0,
                    "serving_unit": "cup",
                    "calories": 150,
                    "protein_g": 8,
                    "carbs_g": 12,
                    "fat_g": 8,
                    "saturated_fat_g": 5,
                    "trans_fat_g": 0,
                    "cholesterol_mg": 35,
                    "sodium_mg": 120,
                    "fiber_g": 0,
                    "sugar_g": 12,
                    "calcium_mg": 300,
                    "cost_per_serving": 0.50,
                    "created_at": "2025-10-26T00:00:00Z",
                    "updated_at": "2025-10-26T00:00:00Z"
                }
            ]
        }
    }
