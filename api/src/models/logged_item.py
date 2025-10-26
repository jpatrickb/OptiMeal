"""
LoggedItem model - represents a specific quantity of a FoodItem consumed as part of a MealLog.

This model connects MealLog to FoodItem with a serving quantity, allowing
meal nutrition calculations and pantry deductions.
"""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, DECIMAL, ForeignKey, UUID as SQLAlchemyUUID
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from ..db.base import Base


class LoggedItem(Base):
    """A specific quantity of a FoodItem consumed as part of a MealLog."""
    
    __tablename__ = "logged_items"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    meal_log_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("meal_logs.id", ondelete="CASCADE"), nullable=False)
    food_item_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("food_items.id"), nullable=False)
    servings = Column(DECIMAL(10, 2), nullable=False)  # Number of servings consumed
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Relationships
    meal_log = relationship("MealLog", back_populates="logged_items")
    food_item = relationship("FoodItem")
    
    @validates('servings')
    def validate_servings(self, key, servings):
        """Validate servings is greater than 0."""
        if servings is not None and servings <= 0:
            raise ValueError("servings must be greater than 0")
        return servings
    
    @property
    def total_calories(self) -> Optional[Decimal]:
        """Calculate total calories for this logged item."""
        if self.food_item and self.food_item.calories and self.servings:
            return self.food_item.calories * self.servings
        return None
    
    @property
    def total_protein_g(self) -> Optional[Decimal]:
        """Calculate total protein for this logged item."""
        if self.food_item and self.food_item.protein_g and self.servings:
            return self.food_item.protein_g * self.servings
        return None
    
    @property
    def total_carbs_g(self) -> Optional[Decimal]:
        """Calculate total carbohydrates for this logged item."""
        if self.food_item and self.food_item.carbs_g and self.servings:
            return self.food_item.carbs_g * self.servings
        return None
    
    @property
    def total_fat_g(self) -> Optional[Decimal]:
        """Calculate total fat for this logged item."""
        if self.food_item and self.food_item.fat_g and self.servings:
            return self.food_item.fat_g * self.servings
        return None
    
    @property
    def total_cost(self) -> Optional[Decimal]:
        """Calculate total cost for this logged item."""
        if self.food_item and self.food_item.cost_per_serving and self.servings:
            return self.food_item.cost_per_serving * self.servings
        return None
    
    def __repr__(self):
        return f"<LoggedItem(id={self.id}, meal_log_id={self.meal_log_id}, food_item_id={self.food_item_id}, servings={self.servings})>"