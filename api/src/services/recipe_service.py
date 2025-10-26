"""
RecipeService - Business logic for recipe management.

Handles recipe creation, listing, and creation from meal logs.
"""

from decimal import Decimal
from typing import List, Optional, Dict
from uuid import UUID

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_, func

from ..models.recipe import Recipe
from ..models.recipe_ingredient import RecipeIngredient
from ..models.meal_log import MealLog
from ..models.logged_item import LoggedItem
from ..models.food_item import FoodItem
from ..schemas.recipe import (
    RecipeCreate,
    RecipeCreateFromMealLog,
    RecipeResponse,
    RecipeListItem,
    RecipeIngredientResponse,
    RecipeNutritionTotals
)


class RecipeService:
    """Service for managing recipes."""
    
    def __init__(self, db: Session):
        self.db = db

    def create_recipe(self, user_id: UUID, recipe_data: RecipeCreate) -> RecipeResponse:
        """
        Create a new recipe.
        
        Args:
            user_id: ID of the user creating the recipe
            recipe_data: Recipe data including ingredients
            
        Returns:
            Created recipe response
        """
        # Check if recipe name already exists for this user
        existing = self.db.query(Recipe).filter(
            and_(Recipe.user_id == user_id, Recipe.name == recipe_data.name)
        ).first()
        
        if existing:
            raise ValueError(f"Recipe with name '{recipe_data.name}' already exists")
        
        try:
            self.db.begin()
            
            # Create recipe
            recipe = Recipe(
                user_id=user_id,
                name=recipe_data.name,
                description=recipe_data.description
            )
            self.db.add(recipe)
            self.db.flush()  # Get recipe.id
            
            # Add ingredients if provided
            if recipe_data.ingredients:
                for ingredient_data in recipe_data.ingredients:
                    ingredient = RecipeIngredient(
                        recipe_id=recipe.id,
                        food_item_id=ingredient_data.food_item_id,
                        servings=ingredient_data.servings
                    )
                    self.db.add(ingredient)
            
            self.db.commit()
            return self.get_recipe_details(user_id, recipe.id)
            
        except Exception as e:
            self.db.rollback()
            raise e

    def create_from_meal_log(self, user_id: UUID, recipe_data: RecipeCreateFromMealLog) -> RecipeResponse:
        """
        Create a recipe by copying ingredients from a meal log.
        
        Args:
            user_id: ID of the user creating the recipe
            recipe_data: Recipe data with meal log ID to copy from
            
        Returns:
            Created recipe response
        """
        # Check if meal log exists and belongs to user
        meal_log = self.db.query(MealLog).options(
            joinedload(MealLog.logged_items)
        ).filter(
            and_(MealLog.id == recipe_data.meal_log_id, MealLog.user_id == user_id)
        ).first()
        
        if not meal_log:
            raise ValueError("Meal log not found")
        
        if not meal_log.logged_items:
            raise ValueError("Meal log has no items to copy")
        
        # Check if recipe name already exists for this user
        existing = self.db.query(Recipe).filter(
            and_(Recipe.user_id == user_id, Recipe.name == recipe_data.name)
        ).first()
        
        if existing:
            raise ValueError(f"Recipe with name '{recipe_data.name}' already exists")
        
        try:
            self.db.begin()
            
            # Create recipe
            recipe = Recipe(
                user_id=user_id,
                name=recipe_data.name,
                description=recipe_data.description,
                created_from_meal_log_id=recipe_data.meal_log_id
            )
            self.db.add(recipe)
            self.db.flush()  # Get recipe.id
            
            # Copy logged items as recipe ingredients
            for logged_item in meal_log.logged_items:
                ingredient = RecipeIngredient(
                    recipe_id=recipe.id,
                    food_item_id=logged_item.food_item_id,
                    servings=logged_item.servings
                )
                self.db.add(ingredient)
            
            self.db.commit()
            return self.get_recipe_details(user_id, recipe.id)
            
        except Exception as e:
            self.db.rollback()
            raise e

    def get_recipe_details(self, user_id: UUID, recipe_id: UUID) -> Optional[RecipeResponse]:
        """
        Get recipe details with all ingredients.
        
        Args:
            user_id: ID of the user
            recipe_id: ID of the recipe
            
        Returns:
            Recipe response with ingredients, or None if not found
        """
        recipe = self.db.query(Recipe).options(
            joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.food_item)
        ).filter(
            and_(Recipe.id == recipe_id, Recipe.user_id == user_id)
        ).first()
        
        if not recipe:
            return None
        
        # Build ingredients response
        ingredients = []
        for ingredient in recipe.recipe_ingredients:
            ingredients.append(RecipeIngredientResponse(
                id=ingredient.id,
                recipe_id=ingredient.recipe_id,
                food_item_id=ingredient.food_item_id,
                servings=ingredient.servings,
                food_item_name=ingredient.food_item.name,
                food_item_brand=ingredient.food_item.brand,
                food_item_serving_unit=ingredient.food_item.serving_unit,
                total_calories=ingredient.total_calories,
                total_protein_g=ingredient.total_protein_g,
                total_carbs_g=ingredient.total_carbs_g,
                total_fat_g=ingredient.total_fat_g,
                total_cost=ingredient.total_cost,
                created_at=ingredient.created_at
            ))
        
        # Compute nutrition totals
        nutrition_totals = self._compute_nutrition_totals(recipe.recipe_ingredients)
        
        return RecipeResponse(
            id=recipe.id,
            user_id=recipe.user_id,
            name=recipe.name,
            description=recipe.description,
            created_from_meal_log_id=recipe.created_from_meal_log_id,
            ingredients=ingredients,
            nutrition_totals=nutrition_totals,
            created_at=recipe.created_at,
            updated_at=recipe.updated_at
        )

    def list_recipes(
        self, 
        user_id: UUID, 
        page: int = 1, 
        per_page: int = 20, 
        search: Optional[str] = None
    ) -> Dict:
        """
        Get paginated list of recipes for a user.
        
        Args:
            user_id: ID of the user
            page: Page number (1-based)
            per_page: Items per page
            search: Optional search term for recipe name
            
        Returns:
            Dictionary with paginated recipes and metadata
        """
        # Build base query
        query = self.db.query(Recipe).filter(Recipe.user_id == user_id)
        
        # Apply search filter
        if search:
            query = query.filter(Recipe.name.ilike(f"%{search}%"))
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        recipes = query.order_by(desc(Recipe.created_at)).offset(
            (page - 1) * per_page
        ).limit(per_page).all()
        
        # Convert to list response objects
        recipe_items = []
        for recipe in recipes:
            # Get ingredient count
            ingredient_count = self.db.query(RecipeIngredient).filter(
                RecipeIngredient.recipe_id == recipe.id
            ).count()
            
            # Get nutrition totals (simplified query)
            ingredients = self.db.query(RecipeIngredient).options(
                joinedload(RecipeIngredient.food_item)
            ).filter(RecipeIngredient.recipe_id == recipe.id).all()
            
            nutrition_totals = self._compute_nutrition_totals(ingredients)
            
            recipe_items.append(RecipeListItem(
                id=recipe.id,
                user_id=recipe.user_id,
                name=recipe.name,
                description=recipe.description,
                ingredient_count=ingredient_count,
                nutrition_totals=nutrition_totals,
                created_at=recipe.created_at,
                updated_at=recipe.updated_at
            ))
        
        return {
            "recipes": recipe_items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        }

    def update_recipe(self, user_id: UUID, recipe_id: UUID, updates: dict) -> Optional[RecipeResponse]:
        """
        Update a recipe (metadata only, not ingredients).
        
        Args:
            user_id: ID of the user
            recipe_id: ID of the recipe
            updates: Dictionary of fields to update
            
        Returns:
            Updated recipe response, or None if not found
        """
        recipe = self.db.query(Recipe).filter(
            and_(Recipe.id == recipe_id, Recipe.user_id == user_id)
        ).first()
        
        if not recipe:
            return None
        
        # Check for name uniqueness if updating name
        if 'name' in updates and updates['name'] != recipe.name:
            existing = self.db.query(Recipe).filter(
                and_(
                    Recipe.user_id == user_id, 
                    Recipe.name == updates['name'],
                    Recipe.id != recipe_id
                )
            ).first()
            if existing:
                raise ValueError(f"Recipe with name '{updates['name']}' already exists")
        
        # Update allowed fields
        for field, value in updates.items():
            if hasattr(recipe, field) and field in ['name', 'description']:
                setattr(recipe, field, value)
        
        from datetime import datetime
        recipe.updated_at = datetime.utcnow()
        self.db.commit()
        
        return self.get_recipe_details(user_id, recipe_id)

    def delete_recipe(self, user_id: UUID, recipe_id: UUID) -> bool:
        """
        Delete a recipe and all its ingredients.
        
        Args:
            user_id: ID of the user
            recipe_id: ID of the recipe
            
        Returns:
            True if deleted, False if not found
        """
        recipe = self.db.query(Recipe).filter(
            and_(Recipe.id == recipe_id, Recipe.user_id == user_id)
        ).first()
        
        if not recipe:
            return False
        
        # Delete will cascade to recipe_ingredients due to model relationship
        self.db.delete(recipe)
        self.db.commit()
        return True

    def _compute_nutrition_totals(self, recipe_ingredients: List[RecipeIngredient]) -> RecipeNutritionTotals:
        """
        Compute nutrition totals from recipe ingredients.
        
        Args:
            recipe_ingredients: List of recipe ingredients
            
        Returns:
            Aggregated nutrition totals
        """
        total_calories = Decimal('0')
        total_protein_g = Decimal('0')
        total_carbs_g = Decimal('0')
        total_fat_g = Decimal('0')
        total_cost = Decimal('0')
        
        for ingredient in recipe_ingredients:
            if ingredient.total_calories:
                total_calories += ingredient.total_calories
            if ingredient.total_protein_g:
                total_protein_g += ingredient.total_protein_g
            if ingredient.total_carbs_g:
                total_carbs_g += ingredient.total_carbs_g
            if ingredient.total_fat_g:
                total_fat_g += ingredient.total_fat_g
            if ingredient.total_cost:
                total_cost += ingredient.total_cost
        
        return RecipeNutritionTotals(
            total_calories=total_calories if total_calories > 0 else None,
            total_protein_g=total_protein_g if total_protein_g > 0 else None,
            total_carbs_g=total_carbs_g if total_carbs_g > 0 else None,
            total_fat_g=total_fat_g if total_fat_g > 0 else None,
            total_cost=total_cost if total_cost > 0 else None
        )