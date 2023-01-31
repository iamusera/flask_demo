# * utf8
import logging
import logging.config
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml
from loguru import logger
from loguru._logger import Logger
from pydantic import BaseSettings

# class LoggingLevel(str, Enum):
#     """
#     Allowed log levels for the application
#     """
# 
#     CRITICAL: str = "CRITICAL"
#     ERROR: str = "ERROR"
#     WARNING: str = "WARNING"
#     INFO: str = "INFO"
#     DEBUG: str = "DEBUG"
# 
# 
# class LoggingSettings(BaseSettings):
#     """Configure your service logging using a LoggingSettings instance.
# 
#     All arguments are optional.
# 
#     Arguments:
# 
#         level (str): the minimum log-level to log. (default: "DEBUG")
#         format (str): the logformat to use. (default: "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>")
#         filepath (Path): the path where to store the logfiles. (default: None)
#         rotation (str): when to rotate the logfile. (default: "1 days")
#         retention (str): when to remove logfiles. (default: "1 months")
#     """
#     name: str = 'info'
#     level: LoggingLevel = "DEBUG"
#     format: str = (
#         "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
#         "<level>{level: <8}</level> | "
#         "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
#         "<level>{message}</level>"
#     )
#     filepath: Optional[Path] = None
#     rotation: str = "1 days"
#     retention: str = "7 days"
# 
#     class Config:
#         env_prefix = "logging_"
# 
# 
# class InterceptHandler(logging.Handler):
#     def emit(self, record):
#         # Get corresponding Loguru level if it exists
#         try:
#             level = logger.level(record.levelname).name
#         except ValueError:
#             level = record.levelno
# 
#         # Find caller from where originated the logged message
#         frame, depth = logging.currentframe(), 2
#         while frame.f_code.co_filename == logging.__file__:
#             frame = frame.f_back
#             depth += 1
#         logger.opt(depth=depth, exception=record.exc_info).log(
#             level, record.getMessage()
#         )
# 
# 
# def setup_logger(
#     name: str,
#     level: str,
#     format: str,
#     filepath: Optional[Path] = None,
#     rotation: Optional[str] = None,
#     retention: Optional[str] = None,
# ) -> Logger:
# 
#     # Remove loguru default logger
#     logger.remove()
#     # Cath all existing loggers
#     LOGGERS = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
#     # Add stdout logger
#     logger.add(
#         sys.stdout,
#         enqueue=True,
#         colorize=True,
#         backtrace=True,
#         level=level.upper(),
#         format=format,
#     )
#     # Optionally add filepath logger
#     if filepath:
#         Path(filepath).parent.mkdir(parents=True, exist_ok=True)
#         logger.add(
#             str(filepath),
#             rotation=rotation,
#             retention=retention,
#             enqueue=True,
#             colorize=False,
#             backtrace=True,
#             level=level.upper(),
#             format=format,
#         )
#     # Overwrite config of standard library root logger
#     logging.basicConfig(handlers=[InterceptHandler()], level=0)
#     # Overwrite handlers of all existing loggers from standard library logging
#     for _logger in LOGGERS:
#         _logger.handlers = [InterceptHandler()]
#         _logger.propagate = False
# 
#     return logger
# 
# 
# def setup_logger_from_settings(settings: Optional[LoggingSettings] = None) -> Logger:
#     if not settings:
#         settings = LoggingSettings()
#     return setup_logger(
#         settings.name,
#         settings.level,
#         settings.format,
#         settings.filepath,
#         settings.rotation,
#         settings.retention,
#     )

import logging
import os.path

from loguru import logger


class InterceptTimedRotatingFileHandler(logging.Handler):
    """
    自定义反射时间回滚日志记录器
    """

    def __init__(self, filename, when='d', interval=1, backupCount=15, encoding="utf-8", delay=False, utc=False,
                 atTime=None, logging_levels="all"):
        super(InterceptTimedRotatingFileHandler, self).__init__()
        filename = os.path.abspath(filename)
        when = when.lower()
        self.logger_ = logger.bind(sime=filename)
        self.filename = filename
        key_map = {
            'h': 'hour',
            'w': 'week',
            's': 'second',
            'm': 'minute',
            'd': 'day',
        }
        # 根据输入文件格式及时间回滚设立文件名称
        rotation = "%d %s" % (interval, key_map[when])
        retention = "%d %ss" % (backupCount, key_map[when])
        time_format = "{time:%Y-%m-%d_%H-%M-%S}"
        if when == "s":
            time_format = "{time:%Y-%m-%d_%H-%M-%S}"
        elif when == "m":
            time_format = "{time:%Y-%m-%d_%H-%M}"
        elif when == "h":
            time_format = "{time:%Y-%m-%d_%H}"
        elif when == "d":
            time_format = "{time:%Y-%m-%d}"
        elif when == "w":
            time_format = "{time:%Y-%m-%d}"
        level_keys = ["info"]
        levels = {
            # "debug": lambda x: "DEBUG" == x['level'].name.upper() and x['extra'].get('sime') == filename,
            "error": lambda x: "ERROR" == x['level'].name.upper() and x['extra'].get('sime') == filename,
            "info": lambda x: "INFO" == x['level'].name.upper() and x['extra'].get('sime') == filename,
            # "warning": lambda x: "WARNING" == x['level'].name.upper() and x['extra'].get('sime') == filename
        }
        if isinstance(logging_levels, str):
            if logging_levels.lower() == "all":
                level_keys = levels.keys()
            elif logging_levels.lower() in levels:
                level_keys = [logging_levels]
        elif isinstance(logging_levels, (list, tuple)):
            level_keys = logging_levels
        for k, f in {_: levels[_] for _ in level_keys}.items():

            filename_fmt = filename.replace(".log", "_%s_%s.log" % (time_format, k))
            # noinspection PyUnresolvedReferences,PyProtectedMember
            file_key = {_._name: han_id for han_id, _ in self.logger_._core.handlers.items()}
            filename_fmt_key = "'{}'".format(filename_fmt)
            if filename_fmt_key in file_key:
                continue
                # self.logger_.remove(file_key[filename_fmt_key])
            self.logger_.add(
                filename_fmt,
                retention=retention,
                encoding=encoding,
                level=self.level,
                rotation=rotation,
                compression="tar.gz",  # 日志归档自行压缩文件
                delay=delay,
                enqueue=True,
                filter=f
            )

    def emit(self, record):
        try:
            level = self.logger_.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        self.logger_.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class Log:
    def __init__(self):
        self._log_cfg = None

    def init(self, app):
        etc_path = os.path.join(app.config['ROOT_PATH'], 'etc', 'loguru_log.yaml')
        if os.path.exists(etc_path):
            with open(etc_path, "r") as f:
                self._log_cfg = yaml.safe_load(f)
                self.set_log_path(app)
                try:
                    logging.config.dictConfig(self._log_cfg)
                except Exception as e:
                    print(e)
        else:
            logging.basicConfig(level=logging.DEBUG)

    def set_log_path(self, app):
        for key in self._log_cfg["handlers"]:
            if self._log_cfg["handlers"][key].get("filename", None):
                filename = self._log_cfg["handlers"][key]["filename"]
                file_path = os.path.join(app.config['LOG_PATH'], filename)
                Path(file_path).parent.mkdir(parents=True, exist_ok=True)
                self._log_cfg["handlers"][key]["filename"] = file_path

    def get_logger(self, logger_name):
        return logging.getLogger(logger_name)


def init_loguru(app):
    Log().init(app)
