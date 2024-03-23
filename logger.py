import logging
import os
import coloredlogs
from pathlib import Path

LOG_LEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
TRACE_LEVEL = 9
DEBUG_LOG_FMT = '[{asctime}] [{levelname:4}] {name} -- {message}'
DEBUG_LOG_PATH = 'logs/autogpt.log'

logging.addLevelName(TRACE_LEVEL, 'TRACE')


def _trace_fn(self, message=None, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self.log(TRACE_LEVEL, message, *args, **kwargs)


logging.Logger.trace = _trace_fn


def get_logger(name) -> logging.Logger:
    # create logger
    logger = logging.getLogger(name)

    # create console handler and set level to debug
    if not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
        Path(DEBUG_LOG_PATH).parent.mkdir(exist_ok=True)
        fh = logging.FileHandler(DEBUG_LOG_PATH)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(DEBUG_LOG_FMT, style='{')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # set log format
    coloredlogs.install(
        logger=logger,
        level=LOG_LEVEL,
        fmt=DEBUG_LOG_FMT,
        style='{',
        field_styles={
            'asctime': {'faint': True, 'bold': False},
            'name': {'color': 'cyan'},
            'threadName': {'color': 'blue'},
        },
        level_styles={
            'debug': {'faint': True},
            'warning': {'color': 'yellow'},
            'error': {'color': 'red'}
        }
    )

    logger.propagate = False

    return logger
