from flask import Flask

from .init_sqlalchemy import db, init_databases
from .loguru import init_log


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_log(app)
    # init_loguru(app)
