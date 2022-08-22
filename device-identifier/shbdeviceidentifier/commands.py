import sys
from pathlib import Path
from time import sleep

import click
import pandas as pd
from loguru import logger

from .dataloader import DataLoader
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

def train(model_selector, training_data_path, training_labels_path):
    """Trains a ML model."""
    # HACK: refactor all of this

    model = get_model(model_selector)

    load_train_df = {
        "UNKNOWN": lambda x: logger.error(f"Unsupported file extension for: {training_data_path}."),
        "pcap": DataLoader.from_pcap,
        "pcapng": DataLoader.from_pcap,
        "csv": DataLoader.from_csv,
    }[get_file_type(training_data_path)]
    train_df: pd.DataFrame = load_train_df(training_data_path)

    load_label_lookup = {
        "UNKNOWN": lambda x: logger.error(f"Unsupported file extension for: {training_labels_path}."),
        "json": DataLoader.labels_from_json,
    }[get_file_type(training_labels_path)]
    label_lookup = load_label_lookup(training_labels_path)

    target_labels = ["Google-Nest-Mini", "ESP-1DC41C"]

    # TODO: consider dst too
    def get_label(row: pd.Series):
        # Split IP address and port
        key = row.rsplit(":", 1)[0]

        # Check if label is available
        try:
            label = label_lookup.loc[key, "name"]
            # Check if label is a desired target label, aka. a device that is supposed to be identified
            if label not in target_labels:
                label = "NoLabel"
        except KeyError:
            label = "NoLabel"

        return label

    train_labels = train_df["src"].apply(get_label)

    model.train(train_df[["data_len", "stream_id"]], train_labels)

    save_path = DATA_DIR / Path("ml_models/" + model_selector + ".pkl")
    if model.save(save_path):
        logger.success(f"Model {model_selector} saved successfully to {save_path}.")