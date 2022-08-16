from pathlib import Path

from .app_utilities import IDENTIFIER_HOME

query_dir = IDENTIFIER_HOME / "utilities/queries"


def query_file_to_string(file_path: Path) -> str:
    with open(file_path, "r") as f:
        return f.read()


INFLUX_QUERIES = {
    "get_all_devices": query_file_to_string(query_dir / "get_all_devices.flux"),
    "custom_query": query_file_to_string(query_dir / "custom_query.flux"),
}

SQLITE_QUERIES = {
    "custom_query": query_file_to_string(query_dir / "custom_query.sql"),
}

QUERIES = {"influx": INFLUX_QUERIES, "sqlite": SQLITE_QUERIES}
