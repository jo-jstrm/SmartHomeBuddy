import time
from multiprocessing import Process

import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger

from shbdeviceidentifier.commands import start_database, run_rpc_server, read
from shbdeviceidentifier.db import Database
from shbdeviceidentifier.utilities.app_utilities import DATA_DIR


class TestCommands:
    """
    Test class for the commands module.
    Commands not included because they are tested through their contained functions:
     - read
     - run_rpc_server
    """

    @pytest.fixture(scope="class")
    def caplog(self, caplog: LogCaptureFixture):
        handler_id = logger.add(caplog.handler, format="{message}")
        yield caplog
        logger.remove(handler_id)

    @pytest.fixture(scope="class")
    def db(self):
        return Database()

    @pytest.fixture(scope="class")
    def dummy_pcap(self):
        return (DATA_DIR / "pcaps" / "dummy.pcap").as_posix()

    def test_start_database(self, db):
        start_database(db)
        db.start()
        assert db.is_connected()
        db.stop_InfluxDB()

    def test_run_rpc_server(self, db):
        rpc_server_process = Process(target=run_rpc_server, args=(db,), daemon=True)
        rpc_server_process.start()
        time.sleep(2)

        # Send a SIGTERM to the process
        rpc_server_process.terminate()

        # Check if the process and the database are still running
        assert not rpc_server_process.is_alive()
        assert not db.is_connected()

        if rpc_server_process.is_alive():
            rpc_server_process.kill()
            # Check again after SIGKILL
            assert not rpc_server_process.is_alive()
            assert not db.is_connected()

    def test_read(self, db, dummy_pcap, caplog):
        read(db, dummy_pcap, "pcap")
        assert "Wrote" in caplog.text
        assert "Failed to write" not in caplog.text
