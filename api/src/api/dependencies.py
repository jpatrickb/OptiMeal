"""
FastAPI dependencies for authentication and authorization.

Provides reusable dependencies for protecting routes and accessing current user.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.db.base import get_db
from src.models.user import User
from src.utils.auth import decode_access_token

# HTTP Bearer token scheme for extracting JWT from Authorization header
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """
    FastAPI dependency to get the current authenticated user.

    Validates JWT token from Authorization header and returns the user object.

    Args:
        credentials: HTTP Bearer credentials from Authorization header
        db: Database session

    Returns:
        User object for the authenticated user

    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    # Extract token from credentials
    token = credentials.credentials

    # Decode token to get user ID
    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# Type annotation for easier use in routes
CurrentUser = Annotated[User, Depends(get_current_user)]
