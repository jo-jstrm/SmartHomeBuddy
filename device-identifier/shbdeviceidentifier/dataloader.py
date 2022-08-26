from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List, Union, Generator, Tuple, Dict

import pandas as pd
from loguru import logger
from scapy.utils import rdpcap

from .db import Database
from .utilities.app_utilities import resolve_file_path, get_file_type
from .utilities.capture_utilities import convert_Capture_to_DataFrame
from .utilities.logging_utilities import spinner

# noinspection PyPep8Naming
class DataLoader:
    """
    Class for loading data from various sources into a pandas DataFrame.
    """

    @staticmethod
    def from_influxdb(query: str, params: dict = None, bind_params: dict = None) -> pd.DataFrame:
        """
        Loads data from the InfluxDB database.
        """
        client = Database().get_influxdb_client()
        df = (client.query_api().query_data_frame(query, params, bind_params)
                .rename(columns={"_value": "data_len", "_time": "timestamp", "result": "_result"}))
        df = df.drop(columns=[col for col in df.columns if col.startswith("_")], axis=1)
        return df

    @staticmethod
    def from_csv(file_path: Union[Path, str], **kwargs) -> Optional[pd.DataFrame]:
        """
        Loads data from a CSV file.
        """
        file_path = resolve_file_path(file_path)
        if file_path:
            return pd.read_csv(file_path, **kwargs)

    @staticmethod
    def from_pcap(file_path: Union[Path, str]) -> Optional[pd.DataFrame]:
        """
        Loads data from a pcap file.
        """
        file_path = resolve_file_path(file_path)
        # Get the file size in Gigabyte
        file_size = os.path.getsize(file_path) * 1e-9
        spinner_text = "Reading file."
        if file_size > 0.25:
            spinner_text += f" This may take a while, since your file exceeds 250 MB (~{file_size:.2f} GB)."
        spinner.text = spinner_text
        spinner.start()
        if file_path:
            # Read pcap
            cap = rdpcap(file_path.as_posix())
            df = convert_Capture_to_DataFrame(cap)
            if not df.empty:
                return df

    @staticmethod
    def from_generator(generator: Generator) -> Optional[pd.DataFrame]:
        """
        Loads data from a generator.
        """
        ...

    @staticmethod
    def from_dict(data: dict) -> Optional[pd.DataFrame]:
        """
        Constructs a Dataset from data in memory.
        """
        ...

    @staticmethod
    def labels_from_json(file_path: Union[Path, str]) -> Optional[pd.DataFrame]:
        """
        Loads labels from a JSON file.
        """
        file_path = resolve_file_path(file_path)
        if file_path:
            return pd.read_json(file_path, orient="index")
        else:
            return None


def _get_label(row: pd.Series, ip_to_label_map: Dict[str, any], devices_to_train: List[str]) -> str:
    # Split IP address and port
    key = row.rsplit(":", 1)[0]
    # Check if label is available
    try:
        label = ip_to_label_map.loc[key, "name"]
        # Check if label is a desired target label, aka. a device that is supposed to be identified
        if label not in devices_to_train:
            label = "NoLabel"
    except KeyError:
        label = "NoLabel"
    return label

def from_file(training_data_path: str, training_labels_path: str, devices_to_train: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # HACK: refactor all of this
    load_train_df = {
        "UNKNOWN": lambda x: logger.error(f"Unsupported file extension for: {training_data_path}."),
        "pcap": DataLoader.from_pcap,
        "pcapng": DataLoader.from_pcap,
        "csv": DataLoader.from_csv,
    }[get_file_type(training_data_path)]
    X: pd.DataFrame = load_train_df(training_data_path)
    load_label_lookup = {
        "UNKNOWN": lambda x: logger.error(f"Unsupported file extension for: {training_labels_path}."),
        "json": DataLoader.labels_from_json,
    }[get_file_type(training_labels_path)]
    ip_to_label_map = load_label_lookup(training_labels_path)
    Y = X["src"].apply(_get_label, args=(ip_to_label_map, devices_to_train))
    return X, Y

def from_database(query: str, params: str, devices_to_train: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    X = DataLoader.from_influxdb(query, params)
    query = """SELECT device_name, ip_address FROM devices WHERE ip_address not null;"""
    devices = Database().query(query=query, db='sqlite')
    ip_to_label_map = {}
    for device in devices:
        ip_to_label_map[device[1]] = device[0]
    logger.info(f"ip_to_label_map: {ip_to_label_map}")
    Y = X["src"].apply(_get_label, args=(ip_to_label_map, devices_to_train))
    return X,Y