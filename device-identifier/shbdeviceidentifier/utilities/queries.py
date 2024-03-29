from datetime import datetime
from pathlib import Path

from .query_files.custom_query import custom_query
from .query_files.custom_query_flux import custom_query_flux
from .query_files.get_data_flux import get_data_flux


def query_file_to_string(file_path: Path) -> str:
    with open(file_path, "r") as f:
        return f.read()


EARLIEST_TIMESTAMP = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
INFLUX_QUERIES = {"custom_query": custom_query_flux, "get_data": get_data_flux}
SQLITE_QUERIES = {
    "get_all_devices": """SELECT * FROM devices""",
    "custom_query": custom_query,
    "get_latest_capture_file": """SELECT latest_capture_file FROM context;""",
    "set_latest_capture_file": """UPDATE context SET latest_capture_file=? WHERE id=1;""",
    "get_measurement": """SELECT measurement FROM context;""",
    "set_measurement": """UPDATE context SET measurement=? WHERE id=1;""",
    "set_context_defaults": """INSERT INTO context (id, latest_capture_file, measurement) VALUES (1, ?, ?);""",
    "get_device_labels": """SELECT device_name, ip_address FROM devices WHERE measurement==?;""",
    "get_device_name": """SELECT device_name FROM devices WHERE ip_address=? AND measurement=?;""",
    "update_devices": """UPDATE devices SET device_name=? WHERE ip_address=? AND measurement=?;""",
}
QUERIES = {"influx": INFLUX_QUERIES, "sqlite": SQLITE_QUERIES}
