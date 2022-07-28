import functools
import os
import sys
from functools import partial

import click
from loguru import logger
from pyfiglet import Figlet


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
                logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
            result = func(*args, **kwargs)
            if exit_:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper


# ---------------------------------------------------------------------------- #
#                                    App                                       #
# ---------------------------------------------------------------------------- #

from .rpc.server import run_rpc_server

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    auto_envvar_prefix="SHB"
)


class Environment:
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()


pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--version", is_flag=True, help="Show current app version.")
@pass_environment
def app(env, verbose=False, version="0.0.0"):
    """
    SmartHomeBuddy's device identifier.
    """
    figlet = Figlet(font='smslant', justify='left')  # choose btw: small, stampatello, smslant
    click.echo(figlet.renderText('SmartHomeBuddy'))

    run_rpc_server()
