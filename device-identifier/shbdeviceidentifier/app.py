import os
import sys
from dataclasses import dataclass
from functools import partial
from importlib import metadata
from pathlib import Path
from pprint import pprint
from typing import Union

import click
from loguru import logger
from pyfiglet import Figlet

import shbdeviceidentifier.commands as commands
from .db import Database
from .dataloader import DataLoader
from .utilities import get_capture_file_path, Formatter, logger_wraps
from .utilities.ml_utilities import get_model
from .utilities.queries import QUERIES


# ---------------------------------------------------------------------------- #
#                                   Logging                                    #
# ---------------------------------------------------------------------------- #

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
    cwd: str
    version: str
    latest_capture_file: Union[Path, None]
    db: Database

    def __init__(self):
        self.flags = {}
        self.cwd = os.getcwd()
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
    commands.start_database(ctx.db)


# ---------------------------------------------------------------------------- #
#                                 Commands                                     #
# ---------------------------------------------------------------------------- #
@app.command("start")
@logger_wraps()
@pass_ctx
def start(ctx):
    """
    Starts the RPC and database servers.
    """
    commands.run_rpc_server(ctx.db)


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
def read(ctx, file_path: click.Path, file_type: str):
    """Reads all the data from a capture file."""
    file_path = get_capture_file_path(ctx, file_path)
    commands.read(ctx.db, file_path, file_type)


@app.command("identify")
@click.option("-f", "--file_path", type=click.Path(), required=False, default="")
@click.argument("model-path", type=click.Path())
@click.option("-o", "--out", type=click.STRING, required=False, default="stdout")  # TODO: refactor
@click.option("-M", "--model", "model_selector", type=click.STRING, required=False, default="default")
@pass_ctx
@logger_wraps()
def identify(ctx, file_path, model_path, out, model_selector):
    """
    Identifies a device.
    """
    file_path = get_capture_file_path(ctx, file_path)
    df = DataLoader.from_pcap(file_path)

    if not model_selector:
        model_selector = "default"
    model = get_model(model_selector)
    model.load(model_path)

    res = model.predict(df[["data_len", "stream_id"]])
    del df

    if not res.empty:
        logger.success(f"Identified {len(res)} devices.")

    if out == "stdout":
        pprint(res)
    elif out == "sqlite":
        # TODO: write res to sqlite db
        ...
    elif out == "influx" or out == "influxdb":
        # TODO: write res to influxdb
        ...
    elif out == "json":
        # TODO: write res to json file in ctx.home_dir
        ...
    elif out == "csv":
        # TODO: write res to csv file in ctx.home_dir
        ...
    else:
        logger.debug(f"Unknown output format: {out}")


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
    Find all available statements in utilities.query_files.
    """
    statement = QUERIES[data_base][statement_name]
    # TODO: handle long list of results / complex results
    res = ctx.db.query(statement, db=data_base)

    if res:
        # pprint indent does not work with this, probably because of the length of the results
        res = [" " * 57 + f"{i}: {row}" for i, row in enumerate(res)]
        res = "\n".join(res)

        logger.success(f"Query run successfully with the following output: \n" f"{res}")
    else:
        logger.success(f"Query run successfully with no output.")


@app.command("train")
@click.argument("model-selector", nargs=1, type=click.STRING)
@click.argument("training-data-path", nargs=1, type=click.STRING)
@click.argument("training-labels-path", nargs=1, type=click.STRING)
@pass_ctx
@logger_wraps()
def train(ctx, model_selector, training_data_path, training_labels_path):
    """
    Trains a model.
    """
    devices_to_train = ["Google-Nest-Mini", "ESP-1DC41C"]
    commands.traim(model_selector, training_data_path, training_labels_path, devices_to_train)