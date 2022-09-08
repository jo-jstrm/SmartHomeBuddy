# ---------------------------------------------------------------------------- #
#                               Logging Utilities                              #
# ---------------------------------------------------------------------------- #
import functools

from halo import Halo
from loguru import logger

# Define spinner object to be called when waiting for a function,
# without knowing anything about the duration of the execution
spinner = Halo(text="Loading.", spinner="dots")


class Formatter:
    def __init__(self):
        self.padding = 30
        self.fmt = (
            "<light-black>{time:HH:mm:ss} | </>"
            "<light-black>{function}:{line}{extra[padding]} | </>"
            "[<level>{level: ^9}</>] "
            "<level>{message}\n{exception}</>"
        )

    def format(self, record):
        length = len("{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt


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
