#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-03-06 16:22
    @description: 
"""
import logging
import os
from urllib import parse
from application.common.utils import load_yaml, decrypt

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


class Config:
    def __init__(self, etc_path):
        self.etc_path = etc_path
        self.set_attr()

    def set_attr(self):
        cfg = load_yaml(self.etc_path)
        db_cfg = cfg["base"]["database"]

        # 数据库用户名和密码解密
        ext = cfg.get("extra")
        if ext:
            if "db_security_key" in cfg.get("extra"):
                key = cfg["extra"]["db_security_key"]
                if key is not None:
                    user_name = decrypt(cfg["base"]["database"]["username"], key)
                    password = decrypt(cfg["base"]["database"]["password"], key)
                    cfg["base"]["database"]["username"] = parse.quote_plus(user_name)
                    cfg["base"]["database"]["password"] = parse.quote_plus(password)
        # 数据库配置
        # SQLALCHEMY_DATABASE_URI = "oracle://{username}:{password}@{host}:{port}/{service}".format(**db_cfg)
        # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{service}".format(**db_cfg)
        # Config.SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://{username}:{password}@{host}:{port}/{schema}?charset=utf8".format(**db_cfg)
        Config.SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{schema}?charset=utf8".format(
            **db_cfg)
        Config.SQLALCHEMY_ECHO = db_cfg["echo"]
        Config.SQLALCHEMY_POOL_SIZE = db_cfg["pool_size"]
        Config.SQLALCHEMY_MAX_OVERFLOW = db_cfg["max_overflow"]
        Config.SQLALCHEMY_POOL_RECYCLE = db_cfg["pool_recycle"]
        Config.SQLALCHEMY_POOL_TIMEOUT = db_cfg["pool_timeout"]
        Config.SQLALCHEMY_TRACK_MODIFICATIONS = db_cfg["modify"]

        # 默认日志等级
        Config.LOG_LEVEL = logging.INFO
        Config.INFO_LOG = cfg.get('log').get('info')
        Config.ERROR_LOG = cfg.get('log').get('error')

        # celery配置
        Config.CELERY_BROKER_URL = cfg["base"]["redis"]["broker"]
        Config.CELERY_RESULT_BACKEND = cfg["base"]["redis"]["broker"]
        Config.CELERY_TIMEZONE = cfg["base"]["redis"]["timezone"]
        Config.CELERY_IMPORTS = ['application.view.predict_mod.controller']


class DevelopmentConfig(Config):
    etc_path = os.path.join(ROOT_PATH, 'etc', 'dev.yaml')

    def __init__(self):
        super().__init__(os.path.join(ROOT_PATH, 'etc', 'dev.yaml'))
        self.set_attr()


class TestConfig(Config):
    Config.LOG_LEVEL = logging.INFO

    def __init__(self):
        super().__init__(os.path.join(ROOT_PATH, 'etc', 'test.yaml'))
        self.set_attr()


class ProductionConfig(Config):
    def __init__(self):
        super().__init__(os.path.join(ROOT_PATH, 'etc', 'prod.yaml'))
        self.set_attr()
        ProductionConfig.LOG_LEVEL = logging.WARN


class SitConfig(Config):
    def __init__(self):
        super().__init__(os.path.join(ROOT_PATH, 'etc', 'sit.yaml'))
        self.set_attr()
        ProductionConfig.LOG_LEVEL = logging.WARN


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'sit': SitConfig
}
