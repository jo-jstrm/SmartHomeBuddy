import pytest


class TestDatabase:
    """
    Test class for the Database class in the db module.
    """

    def test_start(self, db):
        db.start()
        assert db.is_connected()
        db.stop()
        del db

    def test_stop(self, db):
        db.start()
        db.stop()
        assert not db.is_connected()
        del db

    def test_is_connected(self, db):
        db.start()
        assert db.is_connected()
        assert db.stop()
        assert not db.is_connected()
        del db

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_query_influx_db(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_query_sqlite_db(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_query(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_start_influx_db(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_stop_influx_db(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_write_to_influx_db(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_write_device(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_get_all_devices(self):
        # TODO: implement
        assert True

    # TODO: implement explicit tests for the following methods:
    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__run_influxdb_setup(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__is_influx_db_setup(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__do_initial_db_setup(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__create_sqlite_tables(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__get_influx_db_connection(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__get_influxdb_credentials(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__get_sqlite_connection(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Tested implicitly by other tests.")
    def test__store_influx_db_user(self):
        # TODO: implement
        assert True
