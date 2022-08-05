import functools
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


# ---------------------------------------------------------------------------- #
#                                   Logging                                    #
# ---------------------------------------------------------------------------- #

class Formatter:
    def __init__(self):
        self.padding = 22
        self.fmt = (
            "<light-black>{time:HH:mm:ss} | </>"
            "<light-black>{function}:{line}{extra[padding]}</> | "
            "<level>{level: <8}</> - "
            "<level>{message}\n{exception}</>"
        )

    def format(self, record):
        length = len("{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt


logger.remove()
formatter = Formatter()
config = {"handlers": [{"sink": sys.stdout, "format": formatter.format}]}
logger.configure(**config)
logger.opt = partial(logger.opt, colors=True)


def logger_wraps(*, entry=True, exit_=True, level="DEBUG"):
    """
    The logger_wraps function is a decorator that logs the entry and exit of functions.

    Parameters
    ----------
        *
            Pass a variable number of arguments to a function
        entry=True
            Indicate whether the function should log when it is entered
        exit_=True
            Determine whether to log the exit message
        level="DEBUG"
            Set the level of logging

    Returns
    -------

        A function that wraps the input function

    Examples
    ________

        @logger_wraps(entry=True, exit=True)
        def my_function():
            ...

    Doc Author
    ----------
        TB
    """

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args[1:], kwargs)
            result = func(*args, **kwargs)
            if exit_:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper


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
        self.db = Database()


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
