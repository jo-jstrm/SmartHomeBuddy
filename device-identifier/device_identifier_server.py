import shbdeviceidentifier.db
import shbdeviceidentifier.commands as commands

if __name__ == "__main__":
    db = shbdeviceidentifier.db.Database()
    commands.start_database(db)
    commands.run_rpc_server(db)