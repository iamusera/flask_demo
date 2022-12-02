from flask import Flask

from .init_logger import init_log, LogTimedRotatingFileHandler, InterceptHandler
from .init_sqlalchemy import db, init_databases


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_log(app)
