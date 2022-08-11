from pathlib import Path

q_path = Path("device-identifier/shbdeviceidentifier/utilities/queries").resolve()


def query_file_to_string(file_path: Path) -> str:
    with open(file_path, "r") as f:
        return f.read()


INFLUX_QUERIES = {
    "get_all_devices": query_file_to_string(q_path / "get_all_devices.flux"),
    "custom_query": query_file_to_string(q_path / "custom_query.flux"),
}

SQLITE_QUERIES = {
    "custom_query": query_file_to_string(q_path / "custom_query.sql"),
}

QUERIES = {"influx": INFLUX_QUERIES, "sqlite": SQLITE_QUERIES}
