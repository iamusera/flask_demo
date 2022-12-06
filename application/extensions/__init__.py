from flask import Flask

from .init_logger import init_log
from .init_loguru import init_loguru, InterceptTimedRotatingFileHandler
from .init_sqlalchemy import db, init_databases


def init_plugs(app: Flask) -> None:
    init_databases(app)
    # init_log(app)
    init_loguru(app)