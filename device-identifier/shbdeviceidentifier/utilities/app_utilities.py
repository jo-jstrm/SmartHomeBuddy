from pathlib import Path


# ---------------------------------------------------------------------------- #
#                                App Utilities                                 #
# ---------------------------------------------------------------------------- #

def check_default_capture_file_path(ctx, file_path) -> Path:
    """Handling file path for the default capture file."""
    # filepath supplied by user
    if file_path:
        # Make sure file_path is of correct type and resolves to a valid file
        file_path = file_path if isinstance(file_path, Path) else Path(file_path)
        file_path = file_path.resolve()
        ctx.latest_capture_file = file_path
    # filepath already set
    elif ctx.latest_capture_file:
        file_path = ctx.latest_capture_file
    # filepath not set
    else:
        file_path = Path("./capture.pcap").resolve()
        ctx.latest_capture_file = file_path
    return file_path
