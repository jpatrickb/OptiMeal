"""
Recipe model - represents a user-defined collection of FoodItems saved from a MealLog.

Recipes can be created from logged meals and reused for future meal planning
or logging. They maintain a list of ingredients with specific quantities.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, UUID as SQLAlchemyUUID, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from ..db.base import Base


class Recipe(Base):
    """A user-defined collection of FoodItems saved from a MealLog for reuse."""
    
    __tablename__ = "recipes"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)  # Recipe name like "Mom's Lasagna"
    description = Column(Text, nullable=True)  # Optional description/instructions
    created_from_meal_log_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("meal_logs.id", ondelete="SET NULL"), nullable=True)  # Original meal log if saved from one
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recipes")
    created_from_meal_log = relationship("MealLog", back_populates="recipe")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    # Planned meals relationship will be added in Phase 5 when planning models exist
    
    @validates('name')
    def validate_name(self, key, name):
        """Validate name is not empty."""
        if not name or not name.strip():
            raise ValueError("Recipe name cannot be empty")
        return name.strip()
    
    # Unique constraint for recipe name per user
    __table_args__ = (UniqueConstraint('user_id', 'name', name='uq_user_recipe_name'),)
    
    def __repr__(self):
        return f"<Recipe(id={self.id}, user_id={self.user_id}, name='{self.name}')>"
