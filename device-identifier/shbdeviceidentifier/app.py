import os
import pprint
import sys
from dataclasses import dataclass
from functools import partial
from importlib import metadata
from pathlib import Path
from typing import Union

import click
import pyshark
from loguru import logger
from pyfiglet import Figlet

from .db import Database, DataLoader
from .rpc.server import run_rpc_server
from .utilities import get_capture_file_path, Formatter, logger_wraps, QUERIES

# ---------------------------------------------------------------------------- #
#                                   Logging                                    #
# ---------------------------------------------------------------------------- #
from .utilities.capture_utilities import collect_traffic

logger.remove()
formatter = Formatter()
logger_config = {"handlers": [{"sink": sys.stdout, "format": formatter.format, "level": "SUCCESS"}]}
logger.configure(**logger_config)
logger.opt = partial(logger.opt, colors=True)
logger.level("DEBUG", color="<light-black>")

# ---------------------------------------------------------------------------- #
#                                    App                                       #
# ---------------------------------------------------------------------------- #
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], auto_envvar_prefix="SHB")


@dataclass()
class Context:
    flags: dict
    home: str
    version: str
    latest_capture_file: Union[Path, None]
    db: Database

    def __init__(self):
        self.flags = {}
        self.home = os.getcwd()
        self.version = metadata.version("shbdeviceidentifier")
        self.latest_capture_file = None


pass_ctx = click.make_pass_decorator(Context, ensure=True)
flag_default_options = dict(is_flag=True, default=False, show_default=True)


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=False, chain=True)
@click.option("--debug", "-d", help="Enable debug output.", **flag_default_options)
@click.option("--silent", "-s", help="Disable logging.", **flag_default_options)
@click.option("--verbose", "-v", help="Enable verbose output.", **flag_default_options)
@click.option("--version", "version_flag", help="Show current app version.", **flag_default_options)
@pass_ctx
def app(ctx, debug, silent, verbose, version_flag):
    """
    SmartHomeBuddy's device identifier.
    """
    ctx.flags = dict(debug=debug, silent=silent, verbose=verbose, version_flag=version_flag)

    if version_flag:
        click.echo(f"Version: {ctx.version}")
        sys.exit(0)

    if silent:
        logger.remove()
    else:
        figlet = Figlet(font="smslant", justify="left")  # choose btw: small, stampatello, smslant
        click.echo(figlet.renderText("SmartHomeBuddy"))

    if verbose:
        ctx.verbose = True
        logger_config["handlers"][0]["level"] = "INFO"
        logger.configure(**logger_config)

    if debug:
        logger_config["handlers"][0]["level"] = "DEBUG"
        logger.configure(**logger_config)

    # Database connections checks
    ctx.db = Database()
    if not ctx.db.is_connected():
        logger.error("Database connection failed.")
        sys.exit(1)


# ---------------------------------------------------------------------------- #
#                                 Commands                                     #
# ---------------------------------------------------------------------------- #
@app.command("start")
@logger_wraps()
@pass_ctx
def start(ctx):
    """
    Starts the RPC server.
    """
    try:
        run_rpc_server()
    except KeyboardInterrupt:
        logger.info("Stopping InfluxDB...")
        ctx.db.stop_InfluxDB()


@app.command("collect")
@click.option("-t", "--time", type=click.INT, required=False, default=-1, help="Time to capture in seconds.")
@click.option("-o", "--out", type=click.Path(), required=False, default=None, help="Output file path.")
@click.argument("interface", nargs=1, type=click.STRING)
@pass_ctx
@logger_wraps()
def collect(ctx, interface, time, out):
    """
    Collects all the data from an interface.
    """
    file_path = get_capture_file_path(ctx, out)
    cap = collect_traffic(interface=interface, time=time, output_file=file_path)
    if cap:
        logger.success(f"Captured {len(cap)} packets.")
    else:
        logger.info(f"No packets captured.")


@app.command("show-interfaces")
def show_interfaces():
    """
    The show_interfaces function prints the available interfaces on the machine.
    """
    available_interfaces = {i: Path(face) for i, face in enumerate(pyshark.LiveCapture().interfaces)}
    logger.info(f"Available interfaces:\n {pprint.pformat(available_interfaces, indent=57)[1:-1]}")


@app.command("read")
@click.argument("file_path", type=click.Path())
@click.option(
    "--file-type",
    "-T",
    help="File type to read.",
    required=False,
    type=click.Choice(["pcap", "pcapng"], case_sensitive=False),
    default="pcap",
)
@pass_ctx
@logger_wraps()
def read(ctx, file_path: click.Path, file_type: str) -> None:
    """
    Reads all the data from a capture file.
    """
    file_path = get_capture_file_path(ctx, file_path)

    if file_type == "pcap" or file_type == "pcapng":
        if not DataLoader.from_pcap(file_path, ctx.db).empty:
            logger.success(f"Wrote {file_path} to Database.")
        else:
            logger.error(f"Failed to write {file_path} to Database.")

    # TODO: Add support for other file types.


@app.command("identify")
@click.option("-f", "--file_path", type=click.Path(), required=False, default="")
@click.option("-o", "--out", type=click.Path(), required=False, default="influx")  # TODO: refactor
@pass_ctx
@logger_wraps()
def identify(ctx, file_path, out):
    """
    Identifies a device.
    """
    file_path = get_capture_file_path(ctx, file_path)
    ...


@app.command("query")
@click.option(
    "-D",
    "--data-base",
    help="Choose the database to query.",
    required=False,
    type=click.Choice(["influx", "sqlite"], case_sensitive=False),
    default="influx",
)
@click.argument("statement_name", nargs=1)
@pass_ctx
@logger_wraps()
def query(ctx, data_base, statement_name):
    """
    Queries the database.
    Find all available statements in utilities.queries.
    """
    statement = QUERIES[data_base][statement_name]
    # TODO: handle long list of results / complex results
    res = ctx.db.query(statement, db=data_base)

    if res:
        # pprint indent does not work with this, probably because of the length of the results
        res = [" " * 57 + f"{i}: {row}" for i, row in enumerate(res)]
        res = "\n".join(res)

        logger.info(f"Query run successfully with the following output: \n" f"{res}")

    else:
        logger.info(f"Query run successfully with no output.")