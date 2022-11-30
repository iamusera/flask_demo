from __future__ import absolute_import
import os
from pathlib import Path
import logging
import logging.config
import yaml


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
                    logging.config.dictConfig(self._log_cfg)
                except Exception as e:
                    print(e)
        else:
            logging.basicConfig(level=logging.DEBUG)

    def set_log_path(self, app):
        for key in self._log_cfg["handlers"]:
            if self._log_cfg["handlers"][key].get("filename", None):
                filename = self._log_cfg["handlers"][key]["filename"]
                self._log_cfg["handlers"][key]["filename"] = os.path.join(app.config['LOG_PATH'], filename)

    def get_logger(self, logger_name):
        return logging.getLogger(logger_name)


def init_log(app):
    path = Path(app.config['LOG_PATH'])
    if not path.exists():
        path.mkdir(parents=True)
    Log().init(app)
