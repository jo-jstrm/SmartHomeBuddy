from pathlib import Path
from typing import Union

from loguru import logger


# ---------------------------------------------------------------------------- #
#                                App Utilities                                 #
# ---------------------------------------------------------------------------- #

def get_capture_file_path(ctx, file_path) -> Path:
    """Handling file path for the default capture file."""

    # find existing filepath with priority
    # user supplied filepath > context filepath > default filepath
    paths = (file_path, ctx.latest_capture_file, "device-identifier/shbdeviceidentifier/pcaps/capture.pcap")
    path = next(filter(lambda p: bool(p), paths))

    ctx.latest_capture_file = resolve_file_path(path)
    return ctx.latest_capture_file


def resolve_file_path(file_path: Union[Path, str], error_msg=None) -> Union[Path, None]:
    """ Make sure file_path is of correct type and resolves to a valid file. """
    try:
        file_path = Path(file_path).resolve()
        assert file_path.is_file()
        return file_path
    except Exception as e:
        if error_msg:
            logger.error(error_msg)
        logger.debug(e)
        return None
