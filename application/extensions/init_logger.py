from __future__ import absolute_import
import os
import traceback
from pathlib import Path
import logging
import logging.config
import yaml
from collections import defaultdict
from loguru import logger
from logging.handlers import TimedRotatingFileHandler


class LogTimedRotatingFileHandler(TimedRotatingFileHandler):

    def get_out_logger(self, record):
        trace = logger.add(
            str(self.baseFilename),
            rotation=self.interval,  # 换算成天
            retention=self.backupCount,
            enqueue=True,
            colorize=False,
            backtrace=True,
            level=record.levelname.upper(),
        )
        return trace
    def emit(self, record):
        trace = self.get_out_logger(record)
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
        print(logger)
        logger.remove(trace)

class Log:
    """

    """

    def __init__(self):
        self._log_cfg = None

    def init(self, app):
        etc_path = os.path.join(app.config['ROOT_PATH'], 'etc', 'log.yaml')
        if os.path.exists(etc_path):
            with open(etc_path, "r") as f:
                self._log_cfg = yaml.safe_load(f)
                self.set_log_path(app)
                try:
                    # self.set_handler()
                    # logging.basicConfig(handlers=[InterceptHandler()], level=0)
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

    def set_handler(self):
        loggers = self._log_cfg.get('loggers', defaultdict)
        handlers = self._log_cfg.get('handlers', defaultdict)
        for name, config in loggers.items():
            logger = logging.getLogger(name)
            handler_ = config.get('handlers', defaultdict)
            for hand in handler_:
                handler_class = handlers.get(hand)
                print(1)


def init_log(app):
    try:
        Log().init(app)
    except Exception as e:
        print(traceback.format_exc())
