import logging
import argparse


def _set_log_level() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


def _get_args() -> dict[
    str,
]:
    parser = argparse.AgrumentParser(description="SmartHomeBuddie's device identifier.")
    parser.add_argument(
        "collect", dest="collect_mode", action="store_true", help="Collect network packages."
    )
    parser.set_defaults(collect_mode=False)
    return parser.parse_args()


def main():
    _set_log_level()
    logging.info("Started Python device-identifier.")
    args = _get_args()


if __name__ == "__main__":
    main()
