"""Test module for models."""

from sqlalchemy.orm import sessionmaker


def test_condition_is_true(db_session: sessionmaker) -> None:
    """Test that a condition is true.

    Args:
    ----
        db_session: The database session fixture.
    """
    session = db_session()
    result = session.execute("SELECT 1")
    assert result.fetchone()[0] == 1  # noqa: S101
