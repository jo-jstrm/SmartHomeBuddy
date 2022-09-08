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
from .utilities.queries import EARLIEST_TIMESTAMP


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


def read_labels(db: Database, file_path: click.Path, measurement: str = "main"):
    """Reads all the labels for device IPs from a capture file."""
    labels = DataLoader.labels_from_json(file_path)
    if isinstance(labels, pd.DataFrame) and not labels.empty:

        for ip_address, row in labels.iterrows():
            query = """ INSERT OR IGNORE INTO devices (ip_address, device_name, measurement) VALUES (?, ?, ?) """
            params = (ip_address, row["name"], measurement)
            if db.query_SQLiteDB(query, params) == False:
                return

        logger.trace(f"Labels: {labels}")
        logger.success(f"Wrote labels from {file_path} to Database.")
    else:
        logger.error(f"Failed to read {file_path}.")
        logger.debug(f"Labels: {labels}")


def train(
        model_name,
        use_database: bool,
        training_data_path: str,
        training_labels_path: str,
        devices_to_train: List[str] = None,
        bucket: str = "network_traffic",
        ts_train_start: str = None,
        ts_train_end: str = None,
):
    """Train an ML model."""
    logger.debug(
        "User provided the following parameters for training:"
        f"model_name={model_name}, use_database={use_database}, training_data_path={training_data_path}, "
        f"training_labels_path={training_labels_path}, devices_to_train={devices_to_train}, bucket={bucket}, "
        f"ts_train_start={ts_train_start}, ts_train_end={ts_train_end}"
    )
    if use_database:
        with Database().get_influxdb_client() as client:
            query_api = client.query_api()
            ts_params = {"_start": EARLIEST_TIMESTAMP, "_stop": datetime.now(), "_bucket": bucket}
            if not ts_train_start:
                train_start_query = """
                        from(bucket: _bucket)
                        |> range(start: _start, stop: _stop)
                        |> group()
                        |> first()
                    """
                ts_train_start = query_api.query_data_frame(query=train_start_query, params=ts_params)
                ts_train_start = ts_train_start.iloc[0]["_time"]
            else:
                try:
                    ts_train_start = datetime.strptime(ts_train_start, "%Y-%m-%d %H:%M:%S")
                except:
                    logger.error("Invalid timestamp format for timestamp-train-start. Please use YYYY-MM-DD HH:MM:SS")
            try:
                ts_train_end = datetime.strptime(ts_train_end, "%Y-%m-%d %H:%M:%S") if ts_train_end else datetime.now()
            except:
                logger.error("Invalid timestamp format for timestamp-train-stop. Please use YYYY-MM-DD HH:MM:SS")
        logger.debug(f"Querying train data in time range {ts_train_start} - {ts_train_end}.")
        params = {"_start": ts_train_start, "_stop": ts_train_end, "_bucket": bucket}
        query = """
                    from(bucket: _bucket)
                    |> range(start: _start, stop: _stop)
                    |> filter(fn: (r) => r["_measurement"] == "packet")  
                """
        train_df, train_labels = DataLoader.from_database(query, params, devices_to_train)
    else:
        train_df, train_labels = DataLoader.from_file(training_data_path, training_labels_path, devices_to_train)
    model = get_model(model_name)
    logger.debug("Starting training...")
    model.train(train_df[["data_len", "stream_id"]], train_labels)
    logger.debug("Training finished.")
    save_path = DATA_DIR / Path("ml_models/" + model_name + ".pkl")
    if model.save(save_path):
        logger.success(f"Model {model_name} saved successfully to {save_path}.")
