"""Migration environment setup.

This module sets up the Alembic context for running database migrations.
It configures the database URLs, target metadata, and handles both offline and online migration scenarios.
"""

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app import models

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the database URLs based on environment variables or any other source
url_db1 = os.environ.get("DEV_DATABASE_URL")
url_db2 = os.environ.get("TEST_DATABASE_URL")

# Modify the database URLs in the Alembic config
config.set_section_option("devdb", "sqlalchemy.url", url_db1)
config.set_section_option(
    "testdb",
    "sqlalchemy.url",
    os.environ.get("TEST_DATABASE_URL"),
)

target_metadata = models.Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is acceptable here as well.
    By skipping the Engine creation, we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario, we need to create an Engine and associate a connection with the context.
    """
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
