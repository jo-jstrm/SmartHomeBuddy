from datetime import datetime
from pathlib import Path

from .query_files.custom_query import custom_query
from .query_files.custom_query_flux import custom_query_flux
from .query_files.get_all_devices import get_all_devices


def query_file_to_string(file_path: Path) -> str:
    with open(file_path, "r") as f:
        return f.read()


EARLIEST_TIMESTAMP = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
INFLUX_QUERIES = {
    "custom_query": custom_query_flux,
}
SQLITE_QUERIES = {
    "get_all_devices": get_all_devices,
    "custom_query": custom_query,
}
QUERIES = {"influx": INFLUX_QUERIES, "sqlite": SQLITE_QUERIES}
