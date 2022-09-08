import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger

from shbdeviceidentifier.db import Database


@pytest.fixture(scope="session")
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)


@pytest.fixture(scope="session")
def db():
    """
    Fixture for creating a Database instance.
    """
    return Database()
