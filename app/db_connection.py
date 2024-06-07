"""Module providing database connection and session management using SQLAlchemy.

Sets up the SQLAlchemy engine, session factory, and base class for declarative models.
Also provides a function to get a new database session.
"""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.session import Session

# Constants
DEV_DATABASE_URL = os.getenv("DEV_DATABASE_URL")

# Database setup
engine = create_engine(DEV_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


def get_db_session() -> Generator[Session, None, None]:
    """Get a new database session.

    Yields
    ------
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
