import functools
import sys
from functools import partial

import click
from loguru import logger
from pyfiglet import Figlet


# ---------------------------------------------------------------------------- #
#                               Global definitions                             #
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
config = {
    "handlers": [{"sink": sys.stdout, "format": formatter.format}],
}
logger.configure(**config)
logger.opt = partial(logger.opt, colors=True)


def logger_wraps(*, entry=True, exit_=True, level="DEBUG"):
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


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    auto_envvar_prefix="SHB"
)

# ---------------------------------------------------------------------------- #
#                                    App                                       #
# ---------------------------------------------------------------------------- #


from .rpc.server import run_rpc_server


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--version", is_flag=True, help="Show current app version.")
def app(verbose=False, version="0.0.0"):
    """
    SmartHomeBuddie's device identifier.
    \f

    Parameters
    ----------

    Returns
    -------

    Doc Author
    ----------
        TB
    """
    figlet = Figlet(font='smslant', justify='left')  # choose btw: small, stampatello, smslant
    click.echo(figlet.renderText('SmartHomeBuddy'))

    run_rpc_server()
