"""Utilities for database operations."""


import alembic.config
from alembic import command


def migrate_to_db(
    alembic_ini_path: str = "alembic.ini",
    connection: object | None = None,
    revision: str = "head",
) -> None:
    """Migrate the database to the latest revision.

    Args:
    ----
        alembic_ini_path (str): The path to the Alembic configuration file.
        connection (Optional[object]): The database connection to use for migrations.
        revision (str): The revision to migrate to.
    """
    config = alembic.config.Config(alembic_ini_path)
    if connection is not None:
        config.config_ini_section = "testdb"
        command.upgrade(config, revision)
