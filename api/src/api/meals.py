"""
Meals API endpoints.

Provides endpoints for creating and querying meal logs.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.db.base import get_db
from src.models.user import User
from src.schemas.meal_log import (
    MealLogCreate,
    MealLogResponse,
    MealLogListResponse,
    MealLogCreateResponse,
)
from src.services.meal_log_service import MealLogService

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post(
    "",
    response_model=MealLogCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a meal log with items"
)
def create_meal(
    payload: MealLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MealLogCreateResponse:
    service = MealLogService(db)
    meal, warnings = service.create_meal_log(current_user.id, payload)
    return MealLogCreateResponse(meal_log=meal, warnings=warnings)


@router.get(
    "",
    response_model=MealLogListResponse,
    summary="List user's meal history"
)
def list_meals(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    meal_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MealLogListResponse:
    service = MealLogService(db)
    data = service.list_meal_logs(
        user_id=current_user.id,
        page=page,
        per_page=per_page,
        start_date=start_date,
        end_date=end_date,
        meal_type=meal_type,
    )
    return MealLogListResponse(**data)


@router.get(
    "/{meal_id}",
    response_model=MealLogResponse,
    summary="Get meal details with nutrition totals"
)
def get_meal(
    meal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MealLogResponse:
    service = MealLogService(db)
    meal = service.get_meal_log(current_user.id, meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    return meal
