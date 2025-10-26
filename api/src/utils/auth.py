"""
JWT token generation and validation utilities.

Provides functions for creating and verifying JWT access tokens for user authentication.
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt

from src.utils.config import settings


def create_access_token(user_id: UUID, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: UUID of the user to create token for
        expires_delta: Optional custom expiration time.
                      Defaults to ACCESS_TOKEN_EXPIRE_MINUTES from settings.

    Returns:
        Encoded JWT token string
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta

    # Create JWT payload
    to_encode = {
        "sub": str(user_id),  # Subject: user ID
        "exp": expire,         # Expiration time
        "iat": datetime.utcnow(),  # Issued at
    }

    # Encode JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[UUID]:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        User UUID if token is valid, None if invalid or expired
    """
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Extract user ID from subject claim
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            return None

        # Convert string to UUID
        user_id = UUID(user_id_str)
        return user_id

    except (JWTError, ValueError):
        # Token is invalid, expired, or user_id is not a valid UUID
        return None
