"""Utilities for managing Docker containers for testing."""

import logging
import time
from pathlib import Path

import docker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_container_ready(container: docker.models.containers.Container) -> bool:
    """Check if the container is in a running state.

    Args:
    ----
        container (docker.models.containers.Container): The Docker container object.

    Returns:
    -------
        bool: True if the container is running, False otherwise.
    """
    container.reload()
    return container.status == "running"


def wait_for_stable_status(
    container: docker.models.containers.Container,
    stable_duration: int = 3,
    interval: int = 1,
) -> bool:
    """Wait for the container to have a stable running status.

    Args:
    ----
        container (docker.models.containers.Container): The Docker container object.
        stable_duration (int): The total duration to wait for a stable status.
        interval (int): The interval at which to check the container status.

    Returns:
    -------
        bool: True if the container reached a stable state within the duration, False otherwise.
    """
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= stable_duration / interval:
            return True

        time.sleep(interval)
    return False


def start_database_container() -> docker.models.containers.Container:
    """Start and ensure a PostgreSQL Docker container is ready.

    Returns
    -------
        docker.models.containers.Container: The started Docker container object.

    Raises
    ------
        RuntimeError: If the container or PostgreSQL service does not stabilize within the specified time.
    """
    client = docker.from_env()
    scripts_dir = Path("./docker/scripts").resolve()
    container_name = "test-db"

    try:
        existing_container = client.containers.get(container_name)
        logger.info("Container '%s' exists. Stopping and removing...", container_name)
        existing_container.stop()
        existing_container.remove()
        logger.info("Container '%s' stopped and removed", container_name)
    except docker.errors.NotFound:
        logger.info("Container '%s' does not exist.", container_name)

    # Define container configuration
    container_config = {
        "name": container_name,
        "image": "postgres:16.1-alpine3.19",
        "detach": True,
        "ports": {"5432/tcp": "5434"},  # Specify protocol "tcp" explicitly
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
        },
        "volumes": {
            f"{scripts_dir}": {"bind": "/docker-entrypoint-initdb.d", "mode": "rw"},
        },
        "network_mode": "fastapi-development_dev-network",
    }

    # Start Container
    container = client.containers.run(**container_config)

    while not is_container_ready(container):
        time.sleep(1)

    if not wait_for_stable_status(container):
        error_message = "Container did not stabilize within the specified time"
        logger.error(error_message)
        raise RuntimeError(error_message)

    return container
