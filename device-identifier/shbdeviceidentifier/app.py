import argparse
import logging

from .db import Database

log = logging.getLogger("identifier")


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SmartHomeBuddie's device identifier.")
    parser.add_argument(
        "--collect", dest="collect_mode", action="store_true", help="Collect network packages."
    )
    parser.set_defaults(collect_mode=False)
    return parser.parse_args()


def app() -> None:
    log.setLevel(logging.DEBUG)

    log.info("Started Python device-identifier.")
    args = _get_args()

    db = Database()
    if db.check_InfluxDB_connection():
        db.stop_InfluxDB()
        if db.check_InfluxDB_connection():
            db.stop_InfluxDB(kill=True)
