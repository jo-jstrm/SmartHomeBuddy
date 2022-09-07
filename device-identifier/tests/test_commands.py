import pytest

from shbdeviceidentifier.db import Database


class TestCommands:
    """
    Test class for the commands module.
    Commands not included because they are tested through their contained functions:
     - read
     - run_rpc_server
    """

    @pytest.fixture(scope="class")
    def fixture_db(self):
        return Database()

    def test_start_database(self, fixture_db):
        fixture_db.start()
        assert fixture_db.is_connected()
