class TestCommands:
    """
    Test class for the commands module.
    Commands not included because they are tested through their contained functions:
     - read
     - run_rpc_server
    """

    def test_start_database(self, db):
        db.start()
        assert db.is_connected()
        db.stop()
