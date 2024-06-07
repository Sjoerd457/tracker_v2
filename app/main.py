"""main.py.

This module sets up and runs a FastAPI application with logging configured.
It ensures that a `logs` directory exists in the root directory and saves the
application logs (`app.log`) and development logs (`dev.log`) in this directory.

Logging configuration is specified in `logging.conf`, which includes:
- Console logging
- File logging for root logger (`dev.log`)
- File logging for app-specific logger (`app.log`)

Usage:
    To run the application, execute this script directly.
"""

import logging
import logging.config
from pathlib import Path

import uvicorn
from fastapi import FastAPI

# Ensure the logs directory exists
logs_path = Path(__file__).parents[1].resolve() / Path("logs")

if not logs_path.exists():
    logs_path.mkdir(parents=True)

# Configure logging
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app)
