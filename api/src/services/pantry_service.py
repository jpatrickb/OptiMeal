"""
Service layer for PantryItem operations.

Handles CRUD operations and business logic for pantry management.
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from src.models.pantry_item import PantryItem
from src.models.food_item import FoodItem
from src.schemas.pantry_item import PantryItemCreate, PantryItemUpdate


class PantryService:
    """Service for managing pantry items."""

    @staticmethod
    def add_item(db: Session, pantry_data: PantryItemCreate, user_id: UUID) -> PantryItem:
        """
        Add a new item to the user's pantry or update quantity if already exists.

        Args:
            db: Database session
            pantry_data: Pantry item creation data
            user_id: ID of the user

        Returns:
            Created or updated PantryItem instance

        Raises:
            ValueError: If food_item doesn't exist or doesn't belong to user
        """
        # Verify food item exists and belongs to user
        food_item = db.query(FoodItem).filter(
            FoodItem.id == pantry_data.food_item_id,
            FoodItem.user_id == user_id
        ).first()

        if not food_item:
            raise ValueError("Food item not found or does not belong to user")

        # Validate unit matches food item serving unit
        if pantry_data.unit != food_item.serving_unit:
            raise ValueError(
                f"Unit '{pantry_data.unit}' does not match food item serving unit '{food_item.serving_unit}'"
            )

        # Check if pantry item already exists for this user+food combination
        existing_item = db.query(PantryItem).filter(
            PantryItem.user_id == user_id,
            PantryItem.food_item_id == pantry_data.food_item_id
        ).first()

        if existing_item:
            # Update existing item quantity
            existing_item.quantity += pantry_data.quantity
            if pantry_data.expiration_date:
                # Use the earliest expiration date
                if existing_item.expiration_date:
                    existing_item.expiration_date = min(
                        existing_item.expiration_date,
                        pantry_data.expiration_date
                    )
                else:
                    existing_item.expiration_date = pantry_data.expiration_date
            if pantry_data.location:
                existing_item.location = pantry_data.location

            db.commit()
            db.refresh(existing_item)
            return existing_item

        # Create new pantry item
        pantry_dict = pantry_data.model_dump()
        pantry_dict["user_id"] = user_id

        db_pantry_item = PantryItem(**pantry_dict)
        db.add(db_pantry_item)
        db.commit()
        db.refresh(db_pantry_item)

        return db_pantry_item

    @staticmethod
    def get_pantry(
        db: Session,
        user_id: UUID,
        include_food_details: bool = True
    ) -> List[PantryItem]:
        """
        Get all items in the user's pantry.

        Args:
            db: Database session
            user_id: ID of the user
            include_food_details: Whether to eagerly load food item details

        Returns:
            List of PantryItem instances ordered by expiration date
        """
        query = db.query(PantryItem).filter(PantryItem.user_id == user_id)

        if include_food_details:
            query = query.options(joinedload(PantryItem.food_item))

        # Order by expiration date (items expiring soon first, nulls last)
        query = query.order_by(
            PantryItem.expiration_date.asc().nullslast()
        )

        return query.all()

    @staticmethod
    def get_by_id(db: Session, pantry_item_id: UUID, user_id: UUID) -> Optional[PantryItem]:
        """
        Get a pantry item by ID, ensuring it belongs to the user.

        Args:
            db: Database session
            pantry_item_id: ID of the pantry item
            user_id: ID of the user

        Returns:
            PantryItem if found and belongs to user, None otherwise
        """
        return db.query(PantryItem).options(
            joinedload(PantryItem.food_item)
        ).filter(
            PantryItem.id == pantry_item_id,
            PantryItem.user_id == user_id
        ).first()

    @staticmethod
    def update_quantity(
        db: Session,
        pantry_item_id: UUID,
        pantry_data: PantryItemUpdate,
        user_id: UUID
    ) -> Optional[PantryItem]:
        """
        Update a pantry item's quantity or other fields.

        Args:
            db: Database session
            pantry_item_id: ID of the pantry item
            pantry_data: Updated pantry item data
            user_id: ID of the user

        Returns:
            Updated PantryItem if found, None otherwise

        Raises:
            ValueError: If quantity is negative or unit validation fails
        """
        db_pantry_item = PantryService.get_by_id(db, pantry_item_id, user_id)
        if not db_pantry_item:
            return None

        # Update fields (only those provided)
        update_data = pantry_data.model_dump(exclude_unset=True)

        # Validate unit if provided
        if "unit" in update_data and update_data["unit"]:
            if update_data["unit"] != db_pantry_item.food_item.serving_unit:
                raise ValueError(
                    f"Unit '{update_data['unit']}' does not match food item serving unit "
                    f"'{db_pantry_item.food_item.serving_unit}'"
                )

        # Ensure quantity is non-negative
        if "quantity" in update_data and update_data["quantity"] < 0:
            raise ValueError("Quantity cannot be negative")

        for field, value in update_data.items():
            setattr(db_pantry_item, field, value)

        db.commit()
        db.refresh(db_pantry_item)

        return db_pantry_item

    @staticmethod
    def delete_item(db: Session, pantry_item_id: UUID, user_id: UUID) -> bool:
        """
        Delete an item from the pantry.

        Args:
            db: Database session
            pantry_item_id: ID of the pantry item
            user_id: ID of the user

        Returns:
            True if deleted, False if not found
        """
        db_pantry_item = PantryService.get_by_id(db, pantry_item_id, user_id)
        if not db_pantry_item:
            return False

        db.delete(db_pantry_item)
        db.commit()

        return True

    @staticmethod
    def get_expiring_soon(
        db: Session,
        user_id: UUID,
        days: int = 3
    ) -> List[PantryItem]:
        """
        Get pantry items expiring within specified days.

        Args:
            db: Database session
            user_id: ID of the user
            days: Number of days to look ahead

        Returns:
            List of PantryItem instances expiring soon
        """
        from datetime import timedelta

        today = date.today()
        threshold = today + timedelta(days=days)

        return db.query(PantryItem).options(
            joinedload(PantryItem.food_item)
        ).filter(
            PantryItem.user_id == user_id,
            PantryItem.expiration_date.isnot(None),
            and_(
                PantryItem.expiration_date >= today,
                PantryItem.expiration_date <= threshold
            )
        ).order_by(PantryItem.expiration_date.asc()).all()

    @staticmethod
    def deduct_quantity(
        db: Session,
        food_item_id: UUID,
        servings: Decimal,
        user_id: UUID
    ) -> tuple[bool, Optional[str]]:
        """
        Deduct quantity from pantry when logging a meal.

        Args:
            db: Database session
            food_item_id: ID of the food item
            servings: Number of servings to deduct
            user_id: ID of the user

        Returns:
            Tuple of (success: bool, warning: Optional[str])
            - If pantry item exists and has sufficient quantity: (True, None)
            - If pantry item exists but insufficient quantity: (True, "warning message")
            - If pantry item doesn't exist: (True, "warning message")
        """
        pantry_item = db.query(PantryItem).filter(
            PantryItem.user_id == user_id,
            PantryItem.food_item_id == food_item_id
        ).first()

        if not pantry_item:
            return (True, f"Food item not in pantry - no quantity deducted")

        if pantry_item.quantity >= servings:
            # Sufficient quantity
            pantry_item.quantity -= servings
            db.commit()
            return (True, None)
        else:
            # Insufficient quantity - deduct what's available and warn
            pantry_item.quantity = Decimal(0)
            db.commit()
            return (True, f"Insufficient quantity in pantry - only had {pantry_item.quantity}, needed {servings}")
