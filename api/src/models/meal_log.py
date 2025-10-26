"""
MealLog model - represents a meal eaten by a user at a specific time.

This model stores the metadata about a meal (when, what type, notes)
while the actual food items consumed are stored in LoggedItem.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, UUID as SQLAlchemyUUID
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from ..db.base import Base


class MealLog(Base):
    """A record of a meal eaten by the user at a specific date and time."""
    
    __tablename__ = "meal_logs"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    meal_name = Column(String(255), nullable=True)  # Optional name like "Breakfast", "Lunch"
    meal_type = Column(String(50), nullable=True)  # breakfast, lunch, dinner, snack
    logged_at = Column(DateTime(timezone=True), nullable=False)  # When meal was eaten
    notes = Column(Text, nullable=True)  # Optional notes about the meal
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="meal_logs")
    logged_items = relationship("LoggedItem", back_populates="meal_log", cascade="all, delete-orphan")
    # Feedback relationship will be added in Phase 6 when Feedback model exists
    recipe = relationship("Recipe", back_populates="created_from_meal_log", uselist=False)
    
    @validates('meal_type')
    def validate_meal_type(self, key, meal_type):
        """Validate meal_type is one of the allowed values."""
        if meal_type is not None:
            allowed_types = {'breakfast', 'lunch', 'dinner', 'snack'}
            if meal_type not in allowed_types:
                raise ValueError(f"meal_type must be one of {allowed_types}")
        return meal_type
    
    @validates('logged_at')
    def validate_logged_at(self, key, logged_at):
        """Validate logged_at is not in the future."""
        if logged_at and logged_at > datetime.now(logged_at.tzinfo):
            raise ValueError("logged_at cannot be in the future")
        return logged_at
    
    def __repr__(self):
        return f"<MealLog(id={self.id}, user_id={self.user_id}, meal_type={self.meal_type}, logged_at={self.logged_at})>"