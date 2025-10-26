"""
Recipes API endpoints.

Provides endpoints for creating and querying recipes.
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.db.base import get_db
from src.models.user import User
from src.schemas.recipe import (
    RecipeCreateFromMealLog,
    RecipeCreate,
    RecipeResponse,
    RecipeListResponse,
)
from src.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post(
    "",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Save a meal as a recipe"
)
def create_recipe_from_meal(
    payload: RecipeCreateFromMealLog,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> RecipeResponse:
    service = RecipeService(db)
    try:
        recipe = service.create_from_meal_log(current_user.id, payload)
        return recipe
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "",
    response_model=RecipeListResponse,
    summary="List user's saved recipes"
)
def list_recipes(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> RecipeListResponse:
    service = RecipeService(db)
    data = service.list_recipes(current_user.id, page=page, per_page=per_page, search=search)
    return RecipeListResponse(**data)


@router.get(
    "/{recipe_id}",
    response_model=RecipeResponse,
    summary="Get recipe with ingredients"
)
def get_recipe(
    recipe_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> RecipeResponse:
    service = RecipeService(db)
    recipe = service.get_recipe_details(current_user.id, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe
