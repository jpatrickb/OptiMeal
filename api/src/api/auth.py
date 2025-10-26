"""
Authentication API endpoints.

Provides user registration and login endpoints with JWT token generation.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import CurrentUser
from src.db.base import get_db
from src.models.user import User
from src.schemas.auth import Token, UserCreate, UserLogin, UserResponse
from src.utils.auth import create_access_token
from src.utils.security import hash_password, verify_password

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Register a new user account.

    Creates a new user with hashed password and returns user data (no token).
    Client should call /login endpoint after registration to get access token.

    Args:
        user_data: User registration data (email, password, optional full_name)
        db: Database session

    Returns:
        Created user data (without password)

    Raises:
        HTTPException: 400 if email already exists
    """
    # Check if user with email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Login with email and password to receive JWT access token.

    Validates credentials and returns a JWT token for authentication.
    Token should be included in Authorization header for protected routes.

    Args:
        credentials: Login credentials (email and password)
        db: Database session

    Returns:
        JWT access token and token type

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(user_id=user.id)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """
    Get current authenticated user's information.

    Protected endpoint that returns the user data for the authenticated user.

    Args:
        current_user: Current authenticated user (from JWT token)

    Returns:
        User data (without password)
    """
    return current_user
