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
    "get_latest_capture_file": """SELECT latest_capture_file FROM context;""",
    "set_latest_capture_file": """UPDATE context SET latest_capture_file=? WHERE id=1;""",
    "get_measurement": """SELECT measurement FROM context;""",
    "set_measurement": """UPDATE context SET measurement=? WHERE id=1;""",
    "set_context_defaults": """INSERT INTO context (id, latest_capture_file, measurement) VALUES (1, ?, ?);""",
}
QUERIES = {"influx": INFLUX_QUERIES, "sqlite": SQLITE_QUERIES}
