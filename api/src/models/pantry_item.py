"""
PantryItem model for tracking user's pantry inventory.

An instance of a FoodItem in a user's pantry with quantity and expiration.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Column, CheckConstraint, ForeignKey, DECIMAL, String, Date, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.base import Base


class PantryItem(Base):
    """
    An instance of a FoodItem in a user's pantry with quantity and expiration.

    Attributes:
        id: Unique pantry item identifier
        user_id: Owner of this pantry item
        food_item_id: Reference to the food template
        quantity: Current quantity in pantry (must be >= 0)
        unit: Unit of quantity (matches FoodItem.serving_unit)
        expiration_date: Optional expiration date
        location: Storage location (e.g., "Pantry", "Fridge", "Freezer")

    Relationships:
        user: The user who owns this pantry item
        food_item: The food template this item is based on
    """

    __tablename__ = "pantry_items"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Foreign Keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    food_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("food_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Quantity Information
    quantity = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)

    # Optional Fields
    expiration_date = Column(Date, nullable=True)
    location = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="pantry_items")
    food_item = relationship("FoodItem", back_populates="pantry_items")

    # Constraints
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_pantry_quantity_non_negative"),
        UniqueConstraint("user_id", "food_item_id", name="uq_user_food_item"),
    )

    def __repr__(self) -> str:
        return (
            f"<PantryItem(id={self.id}, user_id={self.user_id}, "
            f"food_item_id={self.food_item_id}, quantity={self.quantity} {self.unit})>"
        )
