"""Setup models for FastAPI project.

Instructions:

- Docker-compose up
- Login to adminer

Now this won't work:
`alembic revision --autogenerate -m "initial"`

This will: you need to specify for what DB
`alembic -n devdb revision --autogenerate -m "Your migration message"`

(Make sure migrations / versions actually exists)

`alembic upgrade head`
-> won't work: need to specify devdb

`alembic -n devdb upgrade head`
-> upgrades to latest version database

Now refresh adminer

So steps: first create migrations, then upgrade to execute.
"""

from sqlalchemy import Column, Integer, String

from .db_connection import Base


class FormData(Base):
    """FormData model for storing form submission data."""

    __tablename__ = "form_data"

    click_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
