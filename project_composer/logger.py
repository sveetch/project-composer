import logging

from . import __pkgname__


def init_logger(name, level, printout=True):
    """
    Initialize app logger to configure its level/handler/formatter/etc..

    Arguments:
        name (str): Logger name used to instanciate and retrieve it.
        level (str): Level name (``debug``, ``info``, etc..) to enable.

    Keyword Arguments:
        printout (bool): If False, logs will never be outputed.

    Returns:
        logging.Logger: Application logger.
    """
    root_logger = logging.getLogger(name)
    root_logger.setLevel(level)

    # Redirect outputs to the void space, mostly for usage within unittests
    if not printout:
        from io import StringIO
        dummystream = StringIO()
        handler = logging.StreamHandler(dummystream)
    # Standard output with optional colored messages
    else:
        try:
            import colorlog
        # If colorlog is not available, turn back to standard formatter
        except ImportError:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%H:%M:%S"
                )
            )
        # If colorlog is available use its formatter
        else:
            handler = logging.StreamHandler()
            handler.setFormatter(
                colorlog.ColoredFormatter(
                    "%(asctime)s - %(log_color)s%(message)s",
                    datefmt="%H:%M:%S"
                )
            )

    root_logger.addHandler(handler)

    return root_logger


class LoggerBase:
    """
    A basic class just to ship the required logger object.

    This class should be at the last position in inheritance definition, since it must
    be called first because next classes may require its ``self.log`` attribute.
    """
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__pkgname__)
