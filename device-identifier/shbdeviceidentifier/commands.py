import sys
from datetime import datetime
from pathlib import Path
from time import sleep

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


def train(db: Database, model_name: str, measurement: str = "main"):
    """Train a Machine Learning model."""

    # Get training data
    bind_params = {
        "_start": EARLIEST_TIMESTAMP,
        "_stop": datetime.now(),
        "_bucket": "network-traffic",
        "_measurement_name": measurement,
    }
    logger.debug(f"Querying train data in time range {bind_params['_start']} - {bind_params['_stop']}.")
    train_df = db.query_InfluxDB(QUERIES["influx"]["get_data"], bind_params=bind_params, df=True)

    # Get lables
    train_labels = db.query_SQLiteDB(QUERIES["sqlite"]["get_device_labels"], (measurement,))

    # Modify the data to be in the format required by the model
    # Drop columns and set time index
    relevant_columns = ["_time", "src", "dst", "stream_id", "data_len", "L4_protocol"]
    train_df = train_df[relevant_columns]
    train_df = train_df.rename(columns={"_time": "timestamp"})
    train_df = train_df.set_index("timestamp")
    # Reformat labels to fit df
    train_labels = {v: k for k, v in train_labels}
    # TODO: Determine how the label is calculated. Currently only the source IP is used.
    #  Furthermore we could add them to the data frame and only supply the model with the column names for the labels.
    #  To add them as columns:
    # train_df['src_label'] = train_df.apply(lambda row: train_labels.get(row['src'].split(":")[0], "NoLabel"), axis=1)
    # train_df['dst_label'] = train_df.apply(lambda row: train_labels.get(row['dst'].split(":")[0], "NoLabel"), axis=1)
    train_labels = train_df.apply(lambda row: train_labels.get(row["src"].split(":")[0], "NoLabel"), axis=1)

    # Retrieving the machine learning model
    model = get_model(model_name)

    # Training
    logger.debug("Starting training...")
    model.train(train_df[["data_len", "stream_id"]], train_labels)
    logger.debug("Training finished.")

    # Save model
    save_path = DATA_DIR / Path("ml_models/" + model_name + ".pkl")
    if model.save(save_path):
        logger.success(f"Model {model_name} saved successfully to {save_path}.")
