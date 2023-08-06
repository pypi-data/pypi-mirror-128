"""
Defines configuration constants.
"""
import os
import logging

LOGGER = logging.getLogger("uvicorn")

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/pytest_agent.db"
MAX_WORKER_PROCESSES = int(os.getenv("MAX_WORKER_PROCESSES", 2))
LOGGER.warning(f"Pytest agent starting with {MAX_WORKER_PROCESSES} workers processes")
