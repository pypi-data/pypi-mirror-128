import logging
import os
from typing import Optional, cast

import colorama
from aiologger.levels import check_level
from pythonjsonlogger import jsonlogger

from ..json import dumps
from .colorful import dumps as colorful_dumps
from .context import AsyncContextLogger, ContextLogger
from .level import SUCCESS

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


def patch() -> None:
    if logging.getLoggerClass() == ContextLogger:
        return

    os.environ["PYCHARM_HOSTED"] = "true"
    colorama.init()

    logging.addLevelName(SUCCESS, "SUCCESS")
    logging.setLoggerClass(ContextLogger)

    logger = logging.getLogger()
    logger.setLevel(logging.getLevelName(os.environ.get("LOGLEVEL", "INFO").upper()))


def getLogger(name: Optional[str] = None, colorful: bool = True) -> ContextLogger:
    patch()
    logger = cast(ContextLogger, logging.getLogger(name))
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(
        jsonlogger.JsonFormatter(
            "%(levelname)s %(filename) %(lineno)s %(message)s",
            json_serializer=colorful_dumps if colorful else dumps,
        )
    )
    logger.addHandler(logHandler)
    return logger


def getAsyncLogger(name: str) -> AsyncContextLogger:
    return AsyncContextLogger.with_default_handlers(
        name=name, level=check_level(os.environ.get("LOGLEVEL", "INFO"))
    )
