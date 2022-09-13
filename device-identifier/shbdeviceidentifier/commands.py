import click
import pandas as pd
import sys
from loguru import logger
from time import sleep

from .utilities.app_utilities import SHB_HOME, DATA_DIR, extract_devices
from .db import Database, DataLoader
from .rpc.server import start_rpc_server


def start_database(db: Database):
    logger.debug(f"SHB_HOME: {SHB_HOME}")
    logger.debug(f"DATA_DIR: {DATA_DIR}")
    db.start()
    sleep(0.5)
    if not db.is_connected():
        logger.error("Database connection failed. Quitting.")
        db.stop_InfluxDB()
        sys.exit(1)


def run_rpc_server(db: Database):
    try:
        start_rpc_server()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt. Stopping InfluxDB...")
    except SystemExit:
        logger.info("System exit. Stopping InfluxDB...")
    finally:
        db.stop_InfluxDB()


def read(db: Database, file_path: click.Path, file_type: str):
    """Reads all the data from a capture file."""
    if file_type == "pcap" or file_type == "pcapng":
        packets = DataLoader.from_pcap(file_path)
        if isinstance(packets, pd.DataFrame) and not packets.empty:
            if db.write_to_InfluxDB(
                packets,
                data_frame_measurement_name="packet",
                data_frame_tag_columns=[
                    "src_address",
                    "src_ip",
                    "src_port",
                    "dst_address",
                    "dst_ip",
                    "dst_port",
                    "L4_protocol",
                    "stream_id",
                ],
            ):
                logger.success(f"Wrote {file_path} to database.")
            else:
                logger.error(f"Failed to write {file_path} to database.")
            extract_devices()
        else:
            logger.error(f"Failed to read {file_path}.")
