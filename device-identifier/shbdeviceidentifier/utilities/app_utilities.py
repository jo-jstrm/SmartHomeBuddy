from pathlib import Path
from typing import Union, Optional

from loguru import logger

# ---------------------------------------------------------------------------- #
#                                App Utilities                                 #
# ---------------------------------------------------------------------------- #
parts = Path(__file__).parts
parents = Path(__file__).parents
if "SmartHomeBuddy" in parts and "device-identifier" in parts:
    # Local dev-setup.
    for idx in range(len(parents)):
        if parents[idx].parts[-1] == "device-identifier":
            DATA_DIR = parents[idx].resolve() / "shbdeviceidentifier"
        elif parents[idx].parts[-1] == "SmartHomeBuddy":
            SHB_HOME = parents[idx].resolve()
elif "smarthomebuddy" in parts and "resources" in parts:
    # Installed together with electron-app.
    for idx in range(len(parents)):
        if parents[idx].parts[-1] == "resources":
            SHB_HOME = parents[idx].resolve()
        DATA_DIR = SHB_HOME / "data"
INFLUXDB_DIR = SHB_HOME / "InfluxData"
SQLITE_DIR = SHB_HOME / "SQLite"
QUERY_DIR = DATA_DIR / "utilities" / "query_files"

def get_capture_file_path(ctx, file_path) -> Path:
    """Handling file path for the default capture file."""

    # find existing filepath with priority
    # user supplied filepath > context filepath > default filepath
    paths = (file_path, ctx.latest_capture_file, DATA_DIR / Path("pcaps/capture.pcap"))
    path = next(filter(lambda p: bool(p), paths))

    ctx.latest_capture_file = resolve_file_path(path)
    return ctx.latest_capture_file


def resolve_file_path(file_path: Union[Path, str], error_msg=None) -> Optional[Path]:
    """Make sure file_path is of correct type and resolves to a valid file."""
    try:
        file_path = Path(file_path).resolve()
        assert file_path.is_file()
        return file_path
    except Exception as e:
        if error_msg:
            logger.error(error_msg)
        logger.debug(e)
        return None


def get_file_type(file_path: Union[Path, str]) -> str:
    """Returns the file type of the given file."""
    file_path = resolve_file_path(file_path)
    if file_path:
        return file_path.suffix[1:]
    return "UNKNOWN"