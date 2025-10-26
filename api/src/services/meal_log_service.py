"""
MealLogService - Business logic for meal logging functionality.

Handles meal creation with automatic pantry deduction, nutrition aggregation,
and transaction management for data consistency.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple, Dict
from uuid import UUID

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_, func

from ..models.meal_log import MealLog
from ..models.logged_item import LoggedItem
from ..models.pantry_item import PantryItem
from ..models.food_item import FoodItem
from ..schemas.meal_log import (
    MealLogCreate, 
    MealLogResponse, 
    MealLogWarning, 
    NutritionTotals,
    LoggedItemResponse
)


class MealLogService:
    """Service for managing meal logs."""
    
    def __init__(self, db: Session):
        self.db = db

    def create_meal_log(self, user_id: UUID, meal_data: MealLogCreate) -> Tuple[MealLogResponse, List[MealLogWarning]]:
        """
        Create a new meal log with pantry deduction and warnings.
        
        Args:
            user_id: ID of the user creating the meal log
            meal_data: Meal log data including items
            
        Returns:
            Tuple of (created meal log, list of warnings)
        """
        warnings = []
        
        try:
            # Start transaction
            self.db.begin()
            
            # Create the meal log record
            meal_log = MealLog(
                user_id=user_id,
                meal_name=meal_data.meal_name,
                meal_type=meal_data.meal_type,
                logged_at=meal_data.logged_at,
                notes=meal_data.notes
            )
            self.db.add(meal_log)
            self.db.flush()  # Get the meal_log.id
            
            # Process each logged item
            for item_data in meal_data.items:
                # Create logged item
                logged_item = LoggedItem(
                    meal_log_id=meal_log.id,
                    food_item_id=item_data.food_item_id,
                    servings=item_data.servings
                )
                self.db.add(logged_item)
                
                # Handle pantry deduction
                warning = self._handle_pantry_deduction(
                    user_id=user_id,
                    food_item_id=item_data.food_item_id,
                    servings_consumed=item_data.servings
                )
                if warning:
                    warnings.append(warning)
            
            # Commit transaction
            self.db.commit()
            
            # Return the created meal log with computed nutrition
            meal_response = self.get_meal_log(user_id, meal_log.id)
            return meal_response, warnings
            
        except Exception as e:
            self.db.rollback()
            raise e

    def _handle_pantry_deduction(self, user_id: UUID, food_item_id: UUID, servings_consumed: Decimal) -> Optional[MealLogWarning]:
        """
        Handle pantry deduction for a consumed food item.
        
        Args:
            user_id: ID of the user
            food_item_id: ID of the food item consumed
            servings_consumed: Number of servings consumed
            
        Returns:
            Warning if insufficient pantry, None otherwise
        """
        # Find pantry item for this food
        pantry_item = self.db.query(PantryItem).filter(
            and_(
                PantryItem.user_id == user_id,
                PantryItem.food_item_id == food_item_id
            )
        ).first()
        
        if not pantry_item:
            # No pantry item - this is okay, user might have eaten out
            return None
        
        # Get food item for warning details
        food_item = self.db.query(FoodItem).filter(FoodItem.id == food_item_id).first()
        
        # Check if sufficient quantity available
        if pantry_item.quantity < servings_consumed:
            # Create warning for insufficient pantry
            warning = MealLogWarning(
                food_item_id=food_item_id,
                food_item_name=food_item.name if food_item else "Unknown",
                requested_servings=servings_consumed,
                available_servings=pantry_item.quantity,
                message=f"Only {pantry_item.quantity} servings available, but {servings_consumed} servings were logged. Pantry quantity set to 0."
            )
            
            # Set pantry quantity to 0
            pantry_item.quantity = Decimal('0')
            pantry_item.updated_at = datetime.utcnow()
            
            return warning
        else:
            # Sufficient quantity - deduct the consumed amount
            pantry_item.quantity -= servings_consumed
            pantry_item.updated_at = datetime.utcnow()
            return None

    def get_meal_log(self, user_id: UUID, meal_log_id: UUID) -> Optional[MealLogResponse]:
        """
        Get a meal log with computed nutrition totals.
        
        Args:
            user_id: ID of the user
            meal_log_id: ID of the meal log
            
        Returns:
            Meal log response with nutrition totals, or None if not found
        """
        meal_log = self.db.query(MealLog).options(
            joinedload(MealLog.logged_items).joinedload(LoggedItem.food_item)
        ).filter(
            and_(MealLog.id == meal_log_id, MealLog.user_id == user_id)
        ).first()
        
        if not meal_log:
            return None
        
        # Build logged items response
        logged_items = []
        for item in meal_log.logged_items:
            logged_items.append(LoggedItemResponse(
                id=item.id,
                food_item_id=item.food_item_id,
                servings=item.servings,
                food_item_name=item.food_item.name,
                food_item_brand=item.food_item.brand,
                total_calories=item.total_calories,
                total_protein_g=item.total_protein_g,
                total_carbs_g=item.total_carbs_g,
                total_fat_g=item.total_fat_g,
                total_cost=item.total_cost,
                created_at=item.created_at
            ))
        
        # Compute nutrition totals
        nutrition_totals = self._compute_nutrition_totals(meal_log.logged_items)
        
        return MealLogResponse(
            id=meal_log.id,
            user_id=meal_log.user_id,
            meal_name=meal_log.meal_name,
            meal_type=meal_log.meal_type,
            logged_at=meal_log.logged_at,
            notes=meal_log.notes,
            logged_items=logged_items,
            nutrition_totals=nutrition_totals,
            created_at=meal_log.created_at,
            updated_at=meal_log.updated_at
        )

    def _compute_nutrition_totals(self, logged_items: List[LoggedItem]) -> NutritionTotals:
        """
        Compute nutrition totals from logged items.
        
        Args:
            logged_items: List of logged items
            
        Returns:
            Aggregated nutrition totals
        """
        total_calories = Decimal('0')
        total_protein_g = Decimal('0')
        total_carbs_g = Decimal('0')
        total_fat_g = Decimal('0')
        total_cost = Decimal('0')
        
        for item in logged_items:
            if item.total_calories:
                total_calories += item.total_calories
            if item.total_protein_g:
                total_protein_g += item.total_protein_g
            if item.total_carbs_g:
                total_carbs_g += item.total_carbs_g
            if item.total_fat_g:
                total_fat_g += item.total_fat_g
            if item.total_cost:
                total_cost += item.total_cost
        
        return NutritionTotals(
            total_calories=total_calories if total_calories > 0 else None,
            total_protein_g=total_protein_g if total_protein_g > 0 else None,
            total_carbs_g=total_carbs_g if total_carbs_g > 0 else None,
            total_fat_g=total_fat_g if total_fat_g > 0 else None,
            total_cost=total_cost if total_cost > 0 else None
        )

    def list_meal_logs(
        self, 
        user_id: UUID, 
        page: int = 1, 
        per_page: int = 20, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        meal_type: Optional[str] = None
    ) -> Dict:
        """
        Get paginated list of meal logs for a user with optional filters.
        
        Args:
            user_id: ID of the user
            page: Page number (1-based)
            per_page: Items per page
            start_date: Optional start date filter
            end_date: Optional end date filter  
            meal_type: Optional meal type filter
            
        Returns:
            Dictionary with paginated meal logs and metadata
        """
        # Build base query
        query = self.db.query(MealLog).filter(MealLog.user_id == user_id)
        
        # Apply filters
        if start_date:
            query = query.filter(MealLog.logged_at >= start_date)
        if end_date:
            query = query.filter(MealLog.logged_at <= end_date)
        if meal_type:
            query = query.filter(MealLog.meal_type == meal_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        meal_logs = query.order_by(desc(MealLog.logged_at)).offset(
            (page - 1) * per_page
        ).limit(per_page).all()
        
        # Convert to response objects
        meals = []
        for meal_log in meal_logs:
            meal_response = self.get_meal_log(user_id, meal_log.id)
            if meal_response:
                meals.append(meal_response)
        
        return {
            "meals": meals,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        }

    def update_meal_log(self, user_id: UUID, meal_log_id: UUID, updates: dict) -> Optional[MealLogResponse]:
        """
        Update a meal log (metadata only, not logged items).
        
        Args:
            user_id: ID of the user
            meal_log_id: ID of the meal log
            updates: Dictionary of fields to update
            
        Returns:
            Updated meal log response, or None if not found
        """
        meal_log = self.db.query(MealLog).filter(
            and_(MealLog.id == meal_log_id, MealLog.user_id == user_id)
        ).first()
        
        if not meal_log:
            return None
        
        # Update allowed fields
        for field, value in updates.items():
            if hasattr(meal_log, field) and field in ['meal_name', 'meal_type', 'notes']:
                setattr(meal_log, field, value)
        
        meal_log.updated_at = datetime.utcnow()
        self.db.commit()
        
        return self.get_meal_log(user_id, meal_log_id)

    def delete_meal_log(self, user_id: UUID, meal_log_id: UUID) -> bool:
        """
        Delete a meal log and all its logged items.
        
        Note: This does NOT restore pantry quantities - deletion is for incorrect logs only.
        
        Args:
            user_id: ID of the user
            meal_log_id: ID of the meal log
            
        Returns:
            True if deleted, False if not found
        """
        meal_log = self.db.query(MealLog).filter(
            and_(MealLog.id == meal_log_id, MealLog.user_id == user_id)
        ).first()
        
        if not meal_log:
            return False
        
        # Delete will cascade to logged_items due to model relationship
        self.db.delete(meal_log)
        self.db.commit()
        return True