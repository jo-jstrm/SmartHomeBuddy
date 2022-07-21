import logging
import argparse
from .rpc.server import run_rpc_server


def _set_log_level() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SmartHomeBuddie's device identifier.")
    parser.add_argument(
        "--collect", dest="collect_mode", action="store_true", help="Collect network packages."
    )
    parser.set_defaults(collect_mode=False)
    return parser.parse_args()


def app() -> None:
    _set_log_level()
    logging.info("Started Python device-identifier.")
    args = _get_args()
    run_rpc_server()
