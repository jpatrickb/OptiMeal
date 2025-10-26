"""
FoodItem model for nutritional information templates.

A template for a type of food, containing nutritional information and cost.
This is user-defined and reusable across pantry, meals, recipes, and plans.
"""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, String, DateTime, DECIMAL, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.base import Base


class FoodItem(Base):
    """
    Food item template with nutritional information.

    This model stores the nutritional profile and cost for a specific food.
    It serves as a template that can be referenced by pantry items, logged items,
    recipe ingredients, and planned items.
    """

    __tablename__ = "food_items"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Foreign Keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Basic Info
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)

    # Serving Information
    serving_size = Column(DECIMAL(10, 2), nullable=False)
    serving_unit = Column(String(50), nullable=False)

    # Macronutrients (per serving)
    calories = Column(DECIMAL(8, 2), nullable=True)
    protein_g = Column(DECIMAL(8, 2), nullable=True)
    carbs_g = Column(DECIMAL(8, 2), nullable=True)
    fat_g = Column(DECIMAL(8, 2), nullable=True)

    # Fat Breakdown
    saturated_fat_g = Column(DECIMAL(8, 2), nullable=True)
    trans_fat_g = Column(DECIMAL(8, 2), nullable=True)
    cholesterol_mg = Column(DECIMAL(8, 2), nullable=True)

    # Micronutrients
    sodium_mg = Column(DECIMAL(8, 2), nullable=True)
    fiber_g = Column(DECIMAL(8, 2), nullable=True)
    sugar_g = Column(DECIMAL(8, 2), nullable=True)
    vitamin_a_mcg = Column(DECIMAL(8, 2), nullable=True)
    vitamin_c_mg = Column(DECIMAL(8, 2), nullable=True)
    calcium_mg = Column(DECIMAL(8, 2), nullable=True)
    iron_mg = Column(DECIMAL(8, 2), nullable=True)

    # Cost
    cost_per_serving = Column(DECIMAL(10, 2), nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="food_items")
    pantry_items = relationship("PantryItem", back_populates="food_item", cascade="all, delete-orphan")
    # logged_items = relationship("LoggedItem", back_populates="food_item")
    # recipe_ingredients = relationship("RecipeIngredient", back_populates="food_item")
    # planned_items = relationship("PlannedItem", back_populates="food_item")
    # shopping_list_items = relationship("ShoppingListItem", back_populates="food_item")

    # Constraints
    __table_args__ = (
        CheckConstraint("serving_size > 0", name="check_serving_size_positive"),
        CheckConstraint("calories >= 0 OR calories IS NULL", name="check_calories_non_negative"),
        CheckConstraint("protein_g >= 0 OR protein_g IS NULL", name="check_protein_non_negative"),
        CheckConstraint("carbs_g >= 0 OR carbs_g IS NULL", name="check_carbs_non_negative"),
        CheckConstraint("fat_g >= 0 OR fat_g IS NULL", name="check_fat_non_negative"),
        CheckConstraint("saturated_fat_g >= 0 OR saturated_fat_g IS NULL", name="check_saturated_fat_non_negative"),
        CheckConstraint("trans_fat_g >= 0 OR trans_fat_g IS NULL", name="check_trans_fat_non_negative"),
        CheckConstraint("cholesterol_mg >= 0 OR cholesterol_mg IS NULL", name="check_cholesterol_non_negative"),
        CheckConstraint("sodium_mg >= 0 OR sodium_mg IS NULL", name="check_sodium_non_negative"),
        CheckConstraint("fiber_g >= 0 OR fiber_g IS NULL", name="check_fiber_non_negative"),
        CheckConstraint("sugar_g >= 0 OR sugar_g IS NULL", name="check_sugar_non_negative"),
        CheckConstraint("vitamin_a_mcg >= 0 OR vitamin_a_mcg IS NULL", name="check_vitamin_a_non_negative"),
        CheckConstraint("vitamin_c_mg >= 0 OR vitamin_c_mg IS NULL", name="check_vitamin_c_non_negative"),
        CheckConstraint("calcium_mg >= 0 OR calcium_mg IS NULL", name="check_calcium_non_negative"),
        CheckConstraint("iron_mg >= 0 OR iron_mg IS NULL", name="check_iron_non_negative"),
        CheckConstraint("cost_per_serving >= 0 OR cost_per_serving IS NULL", name="check_cost_non_negative"),
    )

    def __repr__(self) -> str:
        """String representation of FoodItem."""
        return f"<FoodItem(id={self.id}, name={self.name}, user_id={self.user_id})>"
