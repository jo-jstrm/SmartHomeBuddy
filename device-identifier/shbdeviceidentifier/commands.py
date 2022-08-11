import click
import pandas as pd
from loguru import logger

from .db import Database, DataLoader


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
