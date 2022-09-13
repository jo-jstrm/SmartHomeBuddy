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
from .dataloader import DataLoader
from .db import Database
from .utilities import get_capture_file_path, Formatter, logger_wraps
from .utilities.app_utilities import DATA_DIR, resolve_file_path
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


@dataclass
class Context:
    flags: dict
    cwd: str
    version: str
    _latest_capture_file: Union[Path, None]
    _db: Database
    _measurement: str

    def __init__(self):
        self.flags = {}
        self.cwd = os.getcwd()
        self.version = metadata.version("shbdeviceidentifier")
        self._latest_capture_file = None
        self._measurement = "main"

    @property
    def latest_capture_file(self):
        return self._latest_capture_file

    @latest_capture_file.setter
    def latest_capture_file(self, value):
        self._latest_capture_file = value
        params = (value,)
        if isinstance(value, Path):
            params = (value.as_posix(),)
        self._db.query_SQLiteDB(QUERIES["sqlite"]["set_latest_capture_file"], params)

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self._db = value
        if not self._latest_capture_file:
            latest_capture_res = self._db.query_SQLiteDB(QUERIES["sqlite"]["get_latest_capture_file"])
            if latest_capture_res:
                self._latest_capture_file = Path(latest_capture_res[0][0])
        if not self.measurement:
            self.measurement = self._db.query_SQLiteDB(QUERIES["sqlite"]["get_measurement"])[0][0]

    @property
    def measurement(self):
        return self._measurement

    @measurement.setter
    def measurement(self, value):
        self._measurement = value
        self._db.query_SQLiteDB(QUERIES["sqlite"]["set_measurement"], (value,))


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
    db = Database()
    commands.start_database(db)
    ctx.db = db


# ---------------------------------------------------------------------------- #
#                                 Commands                                     #
# ---------------------------------------------------------------------------- #
@app.command("start")
@pass_ctx
@logger_wraps()
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
@click.option(
    "--measurement", "-m", help="Name of the measurement in the InfluxDB. Defaults to `main`.", required=False
)
@pass_ctx
@logger_wraps()
def read(ctx, file_path: click.Path, file_type: str, measurement: str):
    """Reads all the data from a capture file."""
    file_path = get_capture_file_path(ctx, file_path)
    if measurement:
        ctx.measurement = measurement
    commands.read(ctx.db, file_path, file_type, ctx.measurement)


@app.command("read-labels")
@click.argument("file_path", type=click.Path(), required=False, default=DATA_DIR / "pcaps" / "dummy_labels.json")
@click.option(
    "--measurement", "-m", help="Name of the measurement in the InfluxDB. Defaults to `main`.", required=False
)
@pass_ctx
@logger_wraps()
def read_labels(ctx, file_path: click.Path, measurement: str):
    file_path = resolve_file_path(file_path)
    if measurement:
        ctx.measurement = measurement
    commands.read_labels(ctx.db, file_path, ctx.measurement)


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
@click.argument("model-name", nargs=1, type=click.STRING)
@click.option(
    "--measurement", "-m", help="Name of the measurement in the InfluxDB. Defaults to `main`.", required=False
)
@pass_ctx
@logger_wraps()
def train(ctx, model_name, measurement):
    """
    Trains a model.
    """
    if not measurement:
        measurement = ctx.measurement
    # Setting timestamps via the CLI is not supported yet.
    commands.train(model_name=model_name, measurement=measurement)


@app.command("set-measurement")
@click.argument("measurement", nargs=1, type=click.STRING)
@pass_ctx
@logger_wraps()
def set_measurement(ctx, measurement):
    """
    Sets the dataset to use for the current session.
    """
    ctx.measurement = measurement
