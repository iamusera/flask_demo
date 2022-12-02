#* utf8
import logging
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

from loguru import logger
from loguru._logger import Logger
from pydantic import BaseSettings


class LoggingLevel(str, Enum):
    """
    Allowed log levels for the application
    """

    CRITICAL: str = "CRITICAL"
    ERROR: str = "ERROR"
    WARNING: str = "WARNING"
    INFO: str = "INFO"
    DEBUG: str = "DEBUG"


class LoggingSettings(BaseSettings):
    """Configure your service logging using a LoggingSettings instance.

    All arguments are optional.

    Arguments:

        level (str): the minimum log-level to log. (default: "DEBUG")
        format (str): the logformat to use. (default: "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>")
        filepath (Path): the path where to store the logfiles. (default: None)
        rotation (str): when to rotate the logfile. (default: "1 days")
        retention (str): when to remove logfiles. (default: "1 months")
    """

    level: LoggingLevel = "DEBUG"
    format: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    filepath: Optional[Path] = None
    rotation: str = "1 days"
    retention: str = "1 months"

    class Config:
        env_prefix = "logging_"


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logger(
    level: str,
    format: str,
    filepath: Optional[Path] = None,
    rotation: Optional[str] = None,
    retention: Optional[str] = None,
) -> Logger:

    # Remove loguru default logger
    logger.remove()
    # Cath all existing loggers
    LOGGERS = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    # Add stdout logger
    logger.add(
        sys.stdout,
        enqueue=True,
        colorize=True,
        backtrace=True,
        level=level.upper(),
        format=format,
    )
    # Optionally add filepath logger
    if filepath:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            colorize=False,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
    # Overwrite config of standard library root logger
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    # Overwrite handlers of all existing loggers from standard library logging
    for _logger in LOGGERS:
        _logger.handlers = [InterceptHandler()]
        _logger.propagate = False

    return logger


def setup_logger_from_settings(settings: Optional[LoggingSettings] = None) -> Logger:
    if not settings:
        settings = LoggingSettings()
    return setup_logger(
        settings.level,
        settings.format,
        settings.filepath,
        settings.rotation,
        settings.retention,
    )


def init_loguru(app):
    """ 需要加一个配置文件重构一下配置，loguru的logger相当于logging的handler，还要重复的写几个logger才能 """
    setup_logger_from_settings()