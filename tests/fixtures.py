"""Fixtures for setting up the test environment."""

import logging
import os
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.utils.database_utils import migrate_to_db
from tests.utils.docker_utils import start_database_container

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def db_session() -> sessionmaker:
    """Set up the database session for tests.

    Returns
    -------
        sessionmaker: A SQLAlchemy sessionmaker bound to the test database.
    """
    # Add the root of the project to the Python path
    sys.path.append(str(Path(__file__).parent.parent.resolve()))

    start_database_container()

    engine = create_engine(os.getenv("TEST_DATABASE_URL"))

    with engine.begin() as connection:
        migrate_to_db("migrations", "alembic.ini", connection)

    return sessionmaker(autocommit=False, autoflush=True, bind=engine)


if __name__ == "__main__":
    db_session()
