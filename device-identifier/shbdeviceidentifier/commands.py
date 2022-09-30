import sys
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import List

import click
import pandas as pd
from loguru import logger
from numba_progress import ProgressBar

from .dataloader import DataLoader
from .db import Database, extract_devices
from .rpc.server import start_rpc_server
from .utilities.app_utilities import SHB_HOME, DATA_DIR
from .utilities.logging_utilities import spinner, PROGRESS_BAR_FORMAT
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
    logger.info(f"Reading {file_path} for measurement '{measurement}'.")
    if file_type == "pcap" or file_type == "pcapng":
        packets = DataLoader.from_pcap(file_path)
        if isinstance(packets, pd.DataFrame) and not packets.empty:
            if db.write_to_InfluxDB(
                packets,
                data_frame_measurement_name=measurement,
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
            extract_devices(measurement)
        else:
            logger.error(f"Failed to read {file_path}.")


def read_labels(db: Database, file_path: Path, measurement: str = "main"):
    """Reads all the labels for device IPs from a capture file."""
    logger.info(f"Reading labels from {file_path} for measurement '{measurement}'.")

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
        devices_to_train: List[str] = None,
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
    if not devices_to_train:
        devices_to_train = []

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
    if not isinstance(train_df, pd.DataFrame) and not train_df:
        sys.exit(1)

    logger.info(f"Starting training on measurement '{measurement}'. Depending on the model this might take a while.")
    # Retrieve the machine learning model.
    spinner.start(text="Retrieving model...")
    model = get_model(model_name)
    spinner.stop_and_persist(symbol="✅ ".encode("utf-8"), text="Model retrieved.")

    # Model specific data preprocessing.
    spinner.start(text=f"Preparing training data for {model_name}...")
    train_df = model.prepare_train_data(train_df)
    spinner.stop_and_persist(symbol="✅ ".encode("utf-8"), text="Finished preparing data.")

    # Train the model.
    with ProgressBar(
            update_interval=1,
            total=len(model.progress_range) - 1,
            desc=f"   Training {model_name}",
            bar_format=PROGRESS_BAR_FORMAT,
    ) as progress:
        success = model.train(train_df[["data_len", "stream_id"]], train_labels, progress_callback=progress.update)
        # TODO: If progress_callback is not used we might have to call finish() manually.
        # if not progress.finished:
        #     progress.finish()
    if success:
        logger.success("Training finished successfully.")
    else:
        logger.error("Training failed for unknown reasons. Try activating debug mode for more information.")
        return

    # Save model.
    if model.save():
        logger.success(f"Model {model_name} saved successfully to {model.save_path}.")


def identify_devices(db, measurement, model_selector) -> pd.DataFrame:
    model = get_model(model_selector)

    # Load model with internal save path
    # TODO: We should improve the way we handle the save path, maybe we can save the paths in the database?
    model.load()

    logger.info(f"Identifying devices in measurement '{measurement}' using model {model.name}.")

    df, _ = DataLoader.from_database(
        from_timestamp=EARLIEST_TIMESTAMP,
        to_timestamp=datetime.now(),
        measurement=measurement,
        bucket="network-traffic",
        devices_to_train=[],
    )
    if not isinstance(df, pd.DataFrame):
        logger.error("No data found. Exiting.")
        sys.exit(1)
    else:
        # Type hint for linting (Should be obsolete if from_database returns a DataFrame)
        df: pd.DataFrame

    # Get predictions for every row
    res = model.predict(df[["data_len", "stream_id"]])

    # Get majority voting on prediction label for every IP address
    df["prediction"] = res["prediction"]
    res = df[["src_ip", "prediction"]].groupby("src_ip").agg(lambda x: pd.Series.mode(x)[0])
    res["confidence"] = (
        df[["src_ip", "prediction"]].groupby("src_ip").agg(lambda x: x.value_counts().iloc[0] / pd.Series.count(x))
    )

    # Update devices table
    num_named_devices = 0
    for index, row in res.iterrows():
        ip = index
        name = row["prediction"]

        # Skip if it's an unidentified device
        if name == "NoLabel":
            continue

        num_named_devices += 1
        current_name = db.query_SQLiteDB(QUERIES["sqlite"]["get_device_name"], (ip, measurement))[0][0]
        if not current_name:
            if db.query_SQLiteDB(QUERIES["sqlite"]["update_devices"], (name, ip, measurement)):
                logger.trace(f"Updated device {ip} to {name}.")
            else:
                # TODO: Check if this is intended
                #  This happens e.g. if the device is not yet in the devices table.
                logger.debug(f"Could not update device {ip} to {name}.")
        else:
            logger.trace(f"Device {ip} already in devices database as {current_name}.")

    if not res.empty:
        logger.success(f"Identified {num_named_devices} of {len(res)} devices.")
    else:
        logger.info("No devices identified.")

    return res
