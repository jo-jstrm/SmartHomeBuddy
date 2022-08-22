from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List, Union, Generator

import pandas as pd
from scapy.utils import rdpcap

from .db import Database
from .utilities.app_utilities import resolve_file_path
from .utilities.capture_utilities import convert_Capture_to_DataFrame
from .utilities.logging_utilities import spinner

# noinspection PyPep8Naming
class DataLoader:
    """
    Class for loading data from various sources into a pandas DataFrame.
    """

    @staticmethod
    def from_influxdb(self, query: str, params: dict = None, bind_params: dict = None) -> Optional[List]:
        """
        Loads data from the InfluxDB database.
        """
        ...

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