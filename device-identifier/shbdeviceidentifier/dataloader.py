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
    def _from_influxdb(query: str, params: dict = None) -> pd.DataFrame:
        """
        Loads data from the InfluxDB database.
        """
        with Database().get_influxdb_client() as client:
            df = client.query_api().query_data_frame(query=query, params=params)
            # Cannot chain these together, because pandas will complain about missing columns.
            df = df.rename(columns={"_value": "data_len", "_time": "timestamp", "result": "_result"})
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

    @staticmethod
    def from_file(
        training_data_path: str, training_labels_path: str, devices_to_train: List[str]
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Loads train data and labels from a file.
        """
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
        Y = X["src"].apply(_get_label, args=(ip_to_label_map, devices_to_train)).rename("label")
        return X, Y

    @staticmethod
    def from_database(
        train_data_query: str, params: Dict[str:any], devices_to_train: List[str]
    ) -> Union[Tuple[pd.DataFrame, pd.Series], Tuple[None, None]]:
        """
        Loads train data and labels from the database.

        Parameters
        ----------
        train_data_query: str
            The query that retrieves the train data from the database.
        params: Dict[str: any]
            The parameters to be passed to the train data query.
        devices_to_train: List[str]
            The devices that the model should learn to identify.

        Returns
        -------
        Optional[Tuple[pd.DataFrame, pd.Series]]
            Train data and labels.
        """
        X = DataLoader._from_influxdb(train_data_query, params)
        device_query = """SELECT device_name, ip_address FROM devices WHERE ip_address not null;"""
        devices = Database().query(query=device_query, db="sqlite")
        if not devices:
            logger.error("No devices with IP addresses found in the database.")
            return None, None
        logger.debug(f"Devices: {devices}")
        ip_to_label_map = {}
        for device in devices:
            # dict = {ip_address: device_name}
            ip_to_label_map[device[1]] = device[0]
        logger.info(f"ip_to_label_map: {ip_to_label_map}")
        Y = X["src"].apply(_get_label, args=(ip_to_label_map, devices_to_train)).rename("label")
        return X, Y


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
