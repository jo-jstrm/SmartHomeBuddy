import pytest
import pytest_check as check
from _pytest.logging import LogCaptureFixture
from loguru import logger


class TestDatabase:
    """
    Test class for the Database class in the db module.
    """

    @pytest.fixture
    def caplog(self, caplog: LogCaptureFixture):
        handler_id = logger.add(caplog.handler, format="{message}")
        yield caplog
        logger.remove(handler_id)

    @pytest.mark.skip(reason="Temporarily disabled because test fails on GH Action runner.")
    def test_start(self, db):
        db.start()
        check.is_true(db.is_connected())
        db.stop()

    def test_stop(self, db):
        db.start()
        db.stop()
        check.is_true(not db.is_connected())

    @pytest.mark.skip(reason="Temporarily disabled because test fails on GH Action runner.")
    def test_is_connected(self, db):
        db.start()
        check.is_true(db.is_connected())
        check.is_true(db.stop())
        check.is_true(not db.is_connected())

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_query_influx_db(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_query_sqlite_db(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_query(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_start_influx_db(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_stop_influx_db(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_write_to_influx_db(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_write_device(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_get_all_devices(self):
        # TODO: implement
        check.is_true(True)

    # TODO: implement explicit tests for the following methods:
    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__run_influxdb_setup(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__is_influx_db_setup(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__do_initial_db_setup(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__create_sqlite_tables(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__get_influx_db_connection(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__get_influxdb_credentials(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__get_sqlite_connection(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__store_influx_db_user(self):
        # TODO: implement
        check.is_true(True)
