"""
User model for authentication and user management.

Represents an individual using the OptiMeal application.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.base import Base


class User(Base):
    """User account model."""

    __tablename__ = "users"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Profile
    full_name = Column(String(255), nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    food_items = relationship("FoodItem", back_populates="user", cascade="all, delete-orphan")
    pantry_items = relationship("PantryItem", back_populates="user", cascade="all, delete-orphan")
    # meal_logs = relationship("MealLog", back_populates="user", cascade="all, delete-orphan")
    # recipes = relationship("Recipe", back_populates="user", cascade="all, delete-orphan")
    # meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
    # feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    # insights = relationship("Insight", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email={self.email})>"
