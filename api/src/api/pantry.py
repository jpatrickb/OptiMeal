"""
API endpoints for pantry management.

Provides CRUD operations for managing user's pantry inventory.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.db.base import get_db
from src.models.user import User
from src.schemas.pantry_item import (
    PantryItemCreate,
    PantryItemUpdate,
    PantryItemResponse,
    PantryItemWithFoodResponse
)
from src.schemas.base import MessageResponse
from src.services.pantry_service import PantryService

router = APIRouter(prefix="/pantry", tags=["pantry"])


@router.post(
    "",
    response_model=PantryItemWithFoodResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add item to pantry"
)
def add_to_pantry(
    pantry_item: PantryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PantryItemWithFoodResponse:
    """
    Add a food item to the user's pantry.

    If the food item already exists in the pantry, the quantities will be added together.

    **Example:**
    ```json
    {
      "food_item_id": "123e4567-e89b-12d3-a456-426614174000",
      "quantity": 2.5,
      "unit": "cup",
      "expiration_date": "2025-11-15",
      "location": "Fridge"
    }
    ```
    """
    try:
        db_pantry_item = PantryService.add_item(db, pantry_item, current_user.id)
        return PantryItemWithFoodResponse.model_validate(db_pantry_item)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[PantryItemWithFoodResponse],
    summary="Get pantry inventory"
)
def get_pantry(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[PantryItemWithFoodResponse]:
    """
    Get all items in the user's pantry with food details.

    Items are ordered by expiration date (items expiring soon first).
    Items without expiration dates appear last.
    """
    pantry_items = PantryService.get_pantry(
        db,
        user_id=current_user.id,
        include_food_details=True
    )
    return [PantryItemWithFoodResponse.model_validate(item) for item in pantry_items]


@router.get(
    "/expiring-soon",
    response_model=List[PantryItemWithFoodResponse],
    summary="Get items expiring soon"
)
def get_expiring_soon(
    days: int = 3,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[PantryItemWithFoodResponse]:
    """
    Get pantry items expiring within the specified number of days.

    Default is 3 days.
    """
    pantry_items = PantryService.get_expiring_soon(
        db,
        user_id=current_user.id,
        days=days
    )
    return [PantryItemWithFoodResponse.model_validate(item) for item in pantry_items]


@router.get(
    "/{pantry_item_id}",
    response_model=PantryItemWithFoodResponse,
    summary="Get pantry item by ID"
)
def get_pantry_item(
    pantry_item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PantryItemWithFoodResponse:
    """
    Get a specific pantry item by its ID.

    Returns 404 if the pantry item doesn't exist or doesn't belong to the user.
    """
    db_pantry_item = PantryService.get_by_id(db, pantry_item_id, current_user.id)
    if not db_pantry_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pantry item not found"
        )
    return PantryItemWithFoodResponse.model_validate(db_pantry_item)


@router.patch(
    "/{pantry_item_id}",
    response_model=PantryItemWithFoodResponse,
    summary="Update pantry item"
)
def update_pantry_item(
    pantry_item_id: UUID,
    pantry_item: PantryItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PantryItemWithFoodResponse:
    """
    Update a pantry item's quantity, expiration date, or location.

    All fields are optional - only provided fields will be updated.

    **Example:**
    ```json
    {
      "quantity": 1.5,
      "expiration_date": "2025-11-20"
    }
    ```
    """
    try:
        db_pantry_item = PantryService.update_quantity(
            db,
            pantry_item_id,
            pantry_item,
            current_user.id
        )
        if not db_pantry_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pantry item not found"
            )
        return PantryItemWithFoodResponse.model_validate(db_pantry_item)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{pantry_item_id}",
    response_model=MessageResponse,
    summary="Remove item from pantry"
)
def remove_from_pantry(
    pantry_item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MessageResponse:
    """
    Remove an item from the pantry.

    Returns 404 if the pantry item doesn't exist or doesn't belong to the user.
    """
    success = PantryService.delete_item(db, pantry_item_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pantry item not found"
        )
    return MessageResponse(message="Pantry item removed successfully")
