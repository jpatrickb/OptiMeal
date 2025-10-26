"""
API endpoints for food item management.

Provides CRUD operations for food items with nutritional information.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.db.base import get_db
from src.models.user import User
from src.schemas.food_item import FoodItemCreate, FoodItemUpdate, FoodItemResponse
from src.schemas.base import MessageResponse
from src.services.food_item_service import FoodItemService
from src.services.nutrition_ocr_service import NutritionOCRService
from fastapi import File, UploadFile

router = APIRouter(prefix="/food-items", tags=["food-items"])


@router.post(
    "",
    response_model=FoodItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food item"
)
def create_food_item(
    food_item: FoodItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FoodItemResponse:
    """
    Create a new food item with nutritional information.

    **Example:**
    ```json
    {
      "name": "Whole Milk",
      "brand": "Organic Valley",
      "serving_size": 1.0,
      "serving_unit": "cup",
      "calories": 150,
      "protein_g": 8,
      "carbs_g": 12,
      "fat_g": 8
    }
    ```
    """
    try:
        db_food_item = FoodItemService.create(db, food_item, current_user.id)
        return FoodItemResponse.model_validate(db_food_item)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[FoodItemResponse],
    summary="List all food items"
)
def list_food_items(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search term for name or brand"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[FoodItemResponse]:
    """
    Get all food items for the authenticated user.

    Supports pagination and search by name/brand.
    Results are ordered by creation date (most recent first).
    """
    food_items = FoodItemService.get_all(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search
    )
    return [FoodItemResponse.model_validate(item) for item in food_items]


@router.get(
    "/{food_item_id}",
    response_model=FoodItemResponse,
    summary="Get a food item by ID"
)
def get_food_item(
    food_item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FoodItemResponse:
    """
    Get a specific food item by its ID.

    Returns 404 if the food item doesn't exist or doesn't belong to the user.
    """
    db_food_item = FoodItemService.get_by_id(db, food_item_id, current_user.id)
    if not db_food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found"
        )
    return FoodItemResponse.model_validate(db_food_item)


@router.put(
    "/{food_item_id}",
    response_model=FoodItemResponse,
    summary="Update a food item"
)
def update_food_item(
    food_item_id: UUID,
    food_item: FoodItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FoodItemResponse:
    """
    Update a food item's information.

    All fields are optional - only provided fields will be updated.

    **Example:**
    ```json
    {
      "calories": 160,
      "cost_per_serving": 0.55
    }
    ```
    """
    db_food_item = FoodItemService.update(
        db,
        food_item_id,
        food_item,
        current_user.id
    )
    if not db_food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found"
        )
    return FoodItemResponse.model_validate(db_food_item)


@router.delete(
    "/{food_item_id}",
    response_model=MessageResponse,
    summary="Delete a food item"
)
def delete_food_item(
    food_item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MessageResponse:
    """
    Delete a food item.

    Note: This will also cascade delete all related pantry items, logged items,
    recipe ingredients, and planned items.
    """
    success = FoodItemService.delete(db, food_item_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found"
        )
    return MessageResponse(message="Food item deleted successfully")


@router.post(
    "/parse-label",
    summary="Parse nutrition label image using OCR",
    description="Upload an image of a nutrition label to extract calories, protein, carbs, and fat with confidence scores."
)
async def parse_nutrition_label(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = await file.read()
    service = NutritionOCRService(lang="en")
    parsed = service.parse_label(contents)
    # Convert dataclasses to primitives for JSON
    return {k: {"value": v.value, "confidence": v.confidence} for k, v in parsed.items()}
