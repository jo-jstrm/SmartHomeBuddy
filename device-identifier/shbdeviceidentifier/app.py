import os
import os
import sys
from dataclasses import dataclass
from functools import partial
from importlib import metadata
from pathlib import Path
from typing import Union

import click
from loguru import logger
from pyfiglet import Figlet

from .db import Database
from .rpc.server import run_rpc_server
from .utilities import check_default_capture_file_path, Formatter, logger_wraps

# ---------------------------------------------------------------------------- #
#                                   Logging                                    #
# ---------------------------------------------------------------------------- #
logger.remove()
formatter = Formatter()
config = {"handlers": [{"sink": sys.stdout, "format": formatter.format}]}
logger.configure(**config)
logger.opt = partial(logger.opt, colors=True)
logger.level("INFO")


# ---------------------------------------------------------------------------- #
#                                    App                                       #
# ---------------------------------------------------------------------------- #
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    auto_envvar_prefix="SHB"
)


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
        figlet = Figlet(font='smslant', justify='left')  # choose btw: small, stampatello, smslant
        click.echo(figlet.renderText('SmartHomeBuddy'))

    if verbose:
        ctx.verbose = True
        logger.level("INFO")

    if debug:
        logger.level("DEBUG")

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
def start():
    """
    Starts the RPC server.
    """
    run_rpc_server()


@app.command("stop")
@logger_wraps()
def stop():
    """
    Stops the RPC server.
    """
    # TODO: Implement stop command


@app.command("collect")
@click.option("-f", "--file_path", type=click.Path(), required=False, default="")
@pass_ctx
@logger_wraps()
def collect(ctx, file_path):
    """
    Collects all the data from an interface.
    """
    file_path = check_default_capture_file_path(ctx, file_path)
    ...


@app.command("read")
@click.option("-f", "--file_path", type=click.Path(), required=False, default="")
@click.option('--file-type', '-T', help='File type to read.', required=False,
              type=click.Choice(['pcap', 'pcapng'], case_sensitive=False), default='pcap')
@pass_ctx
@logger_wraps()
def read(ctx, file_path, file_type):
    """
    Reads all the data from a capture file.
    """
    file_path = check_default_capture_file_path(ctx, file_path)
    ...


@app.command("identify")
@click.option("-f", "--file_path", type=click.Path(), required=False, default="")
@click.option("-o", "--out", type=click.Path(), required=False, default="influx")  # TODO: refactor
@pass_ctx
@logger_wraps()
def identify(ctx, file_path, out):
    """
    Identifies a device.
    """
    file_path = check_default_capture_file_path(ctx, file_path)
    ...


