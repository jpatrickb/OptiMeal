"""
Service layer for FoodItem operations.

Handles CRUD operations and business logic for food items.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.models.food_item import FoodItem
from src.schemas.food_item import FoodItemCreate, FoodItemUpdate


class FoodItemService:
    """Service for managing food items."""

    @staticmethod
    def create(db: Session, food_item_data: FoodItemCreate, user_id: UUID) -> FoodItem:
        """
        Create a new food item for a user.

        Args:
            db: Database session
            food_item_data: Food item creation data
            user_id: ID of the user creating the food item

        Returns:
            Created FoodItem instance

        Raises:
            ValueError: If validation fails
        """
        # Convert Pydantic model to dict and add user_id
        food_item_dict = food_item_data.model_dump()
        food_item_dict["user_id"] = user_id

        # Create new food item
        db_food_item = FoodItem(**food_item_dict)
        db.add(db_food_item)
        db.commit()
        db.refresh(db_food_item)

        return db_food_item

    @staticmethod
    def get_by_id(db: Session, food_item_id: UUID, user_id: UUID) -> Optional[FoodItem]:
        """
        Get a food item by ID, ensuring it belongs to the user.

        Args:
            db: Database session
            food_item_id: ID of the food item
            user_id: ID of the user

        Returns:
            FoodItem if found and belongs to user, None otherwise
        """
        return db.query(FoodItem).filter(
            FoodItem.id == food_item_id,
            FoodItem.user_id == user_id
        ).first()

    @staticmethod
    def get_all(
        db: Session,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[FoodItem]:
        """
        Get all food items for a user with optional search.

        Args:
            db: Database session
            user_id: ID of the user
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            search: Optional search term for name/brand

        Returns:
            List of FoodItem instances
        """
        query = db.query(FoodItem).filter(FoodItem.user_id == user_id)

        # Apply search filter if provided
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    FoodItem.name.ilike(search_term),
                    FoodItem.brand.ilike(search_term)
                )
            )

        # Order by created_at descending (most recent first)
        query = query.order_by(FoodItem.created_at.desc())

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        food_item_id: UUID,
        food_item_data: FoodItemUpdate,
        user_id: UUID
    ) -> Optional[FoodItem]:
        """
        Update a food item.

        Args:
            db: Database session
            food_item_id: ID of the food item to update
            food_item_data: Updated food item data
            user_id: ID of the user

        Returns:
            Updated FoodItem if found and updated, None otherwise
        """
        # Get existing food item
        db_food_item = FoodItemService.get_by_id(db, food_item_id, user_id)
        if not db_food_item:
            return None

        # Update fields (only those provided)
        update_data = food_item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_food_item, field, value)

        db.commit()
        db.refresh(db_food_item)

        return db_food_item

    @staticmethod
    def delete(db: Session, food_item_id: UUID, user_id: UUID) -> bool:
        """
        Delete a food item.

        Args:
            db: Database session
            food_item_id: ID of the food item to delete
            user_id: ID of the user

        Returns:
            True if deleted, False if not found
        """
        db_food_item = FoodItemService.get_by_id(db, food_item_id, user_id)
        if not db_food_item:
            return False

        db.delete(db_food_item)
        db.commit()

        return True

    @staticmethod
    def count(db: Session, user_id: UUID, search: Optional[str] = None) -> int:
        """
        Count food items for a user.

        Args:
            db: Database session
            user_id: ID of the user
            search: Optional search term

        Returns:
            Count of food items
        """
        query = db.query(FoodItem).filter(FoodItem.user_id == user_id)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    FoodItem.name.ilike(search_term),
                    FoodItem.brand.ilike(search_term)
                )
            )

        return query.count()
