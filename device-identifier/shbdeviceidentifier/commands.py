import sys
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import List

import click
import pandas as pd
from loguru import logger

from .dataloader import DataLoader
from .db import Database
from .rpc.server import start_rpc_server
from .utilities.app_utilities import SHB_HOME, DATA_DIR
from .utilities.ml_utilities import get_model
from .utilities.queries import EARLIEST_TIMESTAMP, QUERIES


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


def read(db: Database, file_path: click.Path, file_type: str, measurement: str = "main"):
    """Reads all the data from a capture file."""
    if file_type == "pcap" or file_type == "pcapng":
        packets = DataLoader.from_pcap(file_path)
        if isinstance(packets, pd.DataFrame) and not packets.empty:
            if db.write_to_InfluxDB(
                packets,
                data_frame_measurement_name=measurement,
                data_frame_tag_columns=["src", "dst", "L4_protocol", "stream_id"],
            ):
                logger.success(f"Wrote {file_path} to Database.")
            else:
                logger.error(f"Failed to write {file_path} to Database.")
        else:
            logger.error(f"Failed to read {file_path}.")


def read_labels(db: Database, file_path: Path, measurement: str = "main"):
    """Reads all the labels for device IPs from a capture file."""
    labels = DataLoader.labels_from_json(file_path)
    if isinstance(labels, pd.DataFrame) and not labels.empty:
        for ip_address, row in labels.iterrows():
            # On duplicate IPs, overwrite device_name and measurement.
            query = """ INSERT INTO devices (ip_address, device_name, measurement) VALUES (?, ?, ?) 
                        ON CONFLICT (ip_address, measurement) DO UPDATE SET device_name = ?, measurement = ?;"""
            params = (ip_address, row["name"], measurement, row["name"], measurement)
            db.query_SQLiteDB(query, params)
        logger.trace(f"Labels: {labels}")
        logger.success(f"Wrote labels from {file_path} to Database.")
    else:
        logger.error(f"Failed to read {file_path}.")
        logger.debug(f"Labels: {labels}")


def train(
    model_name: str,
    measurement: str = "main",
    from_timestamp: str = None,
    to_timestamp: str = None,
    bucket: str = "network-traffic",
    devices_to_train: List[str] = [],
) -> None:
    """Train a Machine Learning model.

    Parameters
    ----------
    model_name: str
        Name of the model to train. Must be implemented in ml_utilities.get_model(). Default is Random Forest.
    measurement: str
        The measurement to train on. Defaults to "main". Measurements are listed in the devices table of the database.
    from_timestamp: str
        The timestamp to start training from. Defaults to the earliest timestamp in the database.
    to_timestamp: str
        The timestamp to stop training at. Defaults to the current time.
    bucket: str
        InfluxDB bucket where the training data is stored. Defaults to "network_traffic".
    devices_to_train: List[str]
        List of devices to train on. When empty, defaults to all devices in the database.

    Returns
    -------
    None
    """
    # Get the data from the database by using the user's input.
    try:
        from_timestamp = (
            datetime.strptime(from_timestamp, "%Y-%m-%d %H:%M:%S") if from_timestamp else EARLIEST_TIMESTAMP
        )
    except Exception:
        logger.info(
            "Invalid timestamp format for 'from_timestamp'. Using earliest possible timestamp instead. "
            "Please use YYYY-MM-DD HH:MM:SS format."
        )
        from_timestamp = EARLIEST_TIMESTAMP
    try:
        to_timestamp = datetime.strptime(to_timestamp, "%Y-%m-%d %H:%M:%S") if to_timestamp else datetime.now()
    except Exception:
        logger.info(
            "Invalid timestamp format for timestamp-train-stop. Using most recent timestamp as instead. "
            "Please use YYYY-MM-DD HH:MM:SS format."
        )
        to_timestamp = datetime.now()
    logger.debug(f"Querying train data in time range {from_timestamp} - {to_timestamp}.")
    train_df, train_labels = DataLoader.from_database(
        from_timestamp, to_timestamp, measurement, bucket, devices_to_train
    )
    # Retrieve the machine learning model.
    model = get_model(model_name)
    # Data preprocessing is model specific.
    train_df = model.prepare_train_data(train_df)
    logger.info("Starting training. This might take a while.")
    model.train(train_df[["data_len", "stream_id"]], train_labels)
    logger.success("Training finished.")
    # Save model.
    time = datetime.now().strftime("%Y%m%d_%H-%M")
    save_path = DATA_DIR / Path(f"ml_models/{time}_{model_name}.pkl")
    if model.save(save_path):
        logger.success(f"Model {model_name} saved successfully to {save_path}.")
