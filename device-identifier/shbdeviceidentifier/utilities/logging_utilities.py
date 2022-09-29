# ---------------------------------------------------------------------------- #
#                               Logging Utilities                              #
# ---------------------------------------------------------------------------- #
import functools
import sys
from functools import partial
from typing import Union

from halo import Halo
from loguru import logger

# Define spinner object to be called when waiting for a function,
# without knowing anything about the duration of the execution
spinner = Halo(text="Loading.", spinner="dots")

# logging levels for loguru
LOG_LEVELS = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
# Format for the tqdm progress bar (numba-progress)
PROGRESS_BAR_FORMAT = "{l_bar}{bar:100}| {n:.0f}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt} {postfix}]{bar:-100b}"


class Formatter:
    def __init__(self, level: Union[int, str] = 3):
        self.padding = 30

        if isinstance(level, str):
            level = LOG_LEVELS.index(level.upper())
        if not 0 <= level <= 5:
            raise ValueError(f"Level must be between 0 and 5 or a level name in {LOG_LEVELS}.")

        if level <= 1:
            self.fmt = (
                "<light-black>{time:HH:mm:ss} | </>"
                "<light-black>{function}:{line}{extra[padding]} | </>"
                "[<level>{level: ^9}</>] "
                "<level>{message}\n{exception}</>"
            )
        elif level == 2:
            self.fmt = "[<level>{level: ^9}</>] " "<level>{message}\n{exception}</>"
        else:
            self.fmt = "{level.icon: <2} <level>{message}\n{exception}</>"

    def format(self, record):
        length = len("{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt


def configure_logging(level: Union[int, str] = 3):
    """
    Configure the logging module for the cli app.
    """
    if isinstance(level, str):
        level = LOG_LEVELS.index(level.upper())
    if not 0 <= level <= 5:
        raise ValueError(f"Level must be between 0 and 5 or a level name in {LOG_LEVELS}.")

    logger.remove()
    formatter = Formatter(level=level)
    logger_config = {"handlers": [{"sink": sys.stdout, "format": formatter.format, "level": LOG_LEVELS[level]}]}
    logger.configure(**logger_config)
    logger.opt = partial(logger.opt, colors=True)
    logger.level("DEBUG", color="<light-black>")
    if level >= 3:
        # logger.level("SUCCESS", color="<light-black>", icon="✔")
        logger.level("SUCCESS", color="<white>", icon="✅")
    else:
        logger.level("SUCCESS", color="<green>")


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
