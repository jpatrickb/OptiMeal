"""
Database configuration and session management for OptiMeal API.

This module provides the SQLAlchemy Base declarative class and database session
dependency for FastAPI dependency injection.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.utils.config import settings

# Create SQLAlchemy engine
# pool_pre_ping ensures connections are alive before use
# echo=True in development for SQL logging
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development",
)

# Create sessionmaker (session factory)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Yields a SQLAlchemy Session and ensures proper cleanup after use.
    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            ...

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
