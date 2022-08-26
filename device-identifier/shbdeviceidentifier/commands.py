import sys
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Tuple, List

import click
import pandas as pd
from loguru import logger

from .dataloader import DataLoader, from_file, from_database
from .db import Database
from .rpc.server import start_rpc_server
from .utilities.ml_utilities import get_model
from .utilities.app_utilities import SHB_HOME, DATA_DIR, get_file_type


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
                data_frame_tag_columns=["src", "dst", "L4_protocol", "stream_id"],
            ):
                logger.success(f"Wrote {file_path} to Database.")
            else:
                logger.error(f"Failed to write {file_path} to Database.")
        else:
            logger.error(f"Failed to read {file_path}.")

def train(model_selector, use_database: bool, training_data_path: str, training_labels_path: str, devices_to_train: List[str]=None):
    """Train an ML model."""
    if use_database:
        params = {
            "_start": datetime.strptime("2022-08-01T11:40:00UTC", "%Y-%m-%dT%H:%M:%S%Z"),
            "_stop": datetime.strptime("2022-08-01T13:41:00UTC", "%Y-%m-%dT%H:%M:%S%Z")
        }
        query = """
                    from(bucket: "network-traffic")
                    |> range(start: _start, stop: _stop)
                    |> filter(fn: (r) => r["_measurement"] == "packet")  
                """
        train_df, train_labels = from_database(query, params, devices_to_train)
    else:
        train_df, train_labels = from_file(training_data_path, training_labels_path, devices_to_train)
    model = get_model(model_selector)
    model.train(train_df[["data_len", "stream_id"]], train_labels)
    save_path = DATA_DIR / Path("ml_models/" + model_selector + ".pkl")
    if model.save(save_path):
        logger.success(f"Model {model_selector} saved successfully to {save_path}.")