"""
Pydantic schemas for PantryItem model.

Schemas for creating, updating, and retrieving pantry items with nested food details.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .food_item import FoodItemResponse


class PantryItemBase(BaseModel):
    """Base schema for PantryItem with common fields."""

    food_item_id: UUID = Field(..., description="Reference to the food item template")
    quantity: Decimal = Field(..., ge=0, description="Current quantity in pantry")
    unit: str = Field(..., min_length=1, max_length=50, description="Unit of quantity")
    expiration_date: Optional[date] = Field(None, description="Optional expiration date")
    location: Optional[str] = Field(None, max_length=100, description="Storage location (e.g., 'Pantry', 'Fridge', 'Freezer')")


class PantryItemCreate(PantryItemBase):
    """Schema for creating a new pantry item."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "food_item_id": "123e4567-e89b-12d3-a456-426614174000",
                    "quantity": 2.5,
                    "unit": "cup",
                    "expiration_date": "2025-11-15",
                    "location": "Fridge"
                }
            ]
        }
    }


class PantryItemUpdate(BaseModel):
    """Schema for updating a pantry item (all fields optional)."""

    quantity: Optional[Decimal] = Field(None, ge=0, description="Updated quantity")
    unit: Optional[str] = Field(None, min_length=1, max_length=50)
    expiration_date: Optional[date] = None
    location: Optional[str] = Field(None, max_length=100)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "quantity": 1.5,
                    "expiration_date": "2025-11-20"
                }
            ]
        }
    }


class PantryItemResponse(PantryItemBase):
    """Schema for pantry item response with database fields."""

    id: UUID = Field(..., description="Unique pantry item identifier")
    user_id: UUID = Field(..., description="Owner of this pantry item")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174002",
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "food_item_id": "123e4567-e89b-12d3-a456-426614174000",
                    "quantity": 2.5,
                    "unit": "cup",
                    "expiration_date": "2025-11-15",
                    "location": "Fridge",
                    "created_at": "2025-10-26T00:00:00Z",
                    "updated_at": "2025-10-26T00:00:00Z"
                }
            ]
        }
    }


class PantryItemWithFoodResponse(PantryItemResponse):
    """Schema for pantry item response with nested food item details."""

    food_item: FoodItemResponse = Field(..., description="Food item details")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174002",
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "food_item_id": "123e4567-e89b-12d3-a456-426614174000",
                    "quantity": 2.5,
                    "unit": "cup",
                    "expiration_date": "2025-11-15",
                    "location": "Fridge",
                    "created_at": "2025-10-26T00:00:00Z",
                    "updated_at": "2025-10-26T00:00:00Z",
                    "food_item": {
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
                        "created_at": "2025-10-26T00:00:00Z",
                        "updated_at": "2025-10-26T00:00:00Z"
                    }
                }
            ]
        }
    }
