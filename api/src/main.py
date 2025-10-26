from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from src.utils.exceptions import (
    OptiMealException,
    optimeal_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from src.utils.logging import RequestLoggingMiddleware

app = FastAPI(
    title="OptiMeal API",
    description="Meal Management Feature - 001",
    version="1.0.0"
)

# Add exception handlers
app.add_exception_handler(OptiMealException, optimeal_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add logging middleware
app.add_middleware(RequestLoggingMiddleware)

# CORS for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "OptiMeal API - Meal Management Feature"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Import and include routers
from src.api import auth, food_items, pantry, meals, recipes

# Authentication routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

# Food Items routes
app.include_router(food_items.router, prefix="/api/v1")

# Pantry routes
app.include_router(pantry.router, prefix="/api/v1")

# Meals routes
app.include_router(meals.router, prefix="/api/v1")

# Recipes routes
app.include_router(recipes.router, prefix="/api/v1")

# Additional routers will be added as they are implemented
# app.include_router(plans.router, prefix="/api/v1/plans", tags=["plans"])
# app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["feedback"])
# app.include_router(insights.router, prefix="/api/v1/insights", tags=["insights"])
