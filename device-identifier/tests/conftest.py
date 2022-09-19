import pytest

from shbdeviceidentifier.db import Database
from shbdeviceidentifier.utilities.app_utilities import DATA_DIR


@pytest.fixture(scope="session")
def db():
    """
    Fixture for creating a Database instance.
    """
    return Database()


@pytest.fixture(scope="session")
def dummy_pcap():
    return (DATA_DIR / "pcaps" / "dummy.pcap").as_posix()


@pytest.fixture(scope="session")
def dummy_csv():
    return (DATA_DIR / "pcaps" / "dummy.csv").as_posix()


@pytest.fixture(scope="session")
def dummy_labels_json():
    return (DATA_DIR / "pcaps" / "dummy_labels.json").as_posix()
