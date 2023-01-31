import logging
import os

from application.common.utils import load_yaml
from application.common.utils.encrypt import decrypt


class DevelopmentConfig:
    ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    etc_path = os.path.join(ROOT_PATH, 'etc', 'dev.yaml')
    cfg = load_yaml(etc_path)

    db_cfg = cfg["base"]["database"]

    # 数据库用户名和密码解密
    ext = cfg.get("extra")
    if ext:
        if "db_security_key" in cfg.get("extra"):
            key = cfg["extra"]["db_security_key"]
            if key is not None:
                cfg["base"]["database"]["username"] = decrypt(cfg["base"]["database"]["username"], key)
                cfg["base"]["database"]["password"] = decrypt(cfg["base"]["database"]["password"], key)
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "oracle://{username}:{password}@{host}:{port}/{service}".format(**db_cfg)
    SQLALCHEMY_ECHO = db_cfg["echo"]
    SQLALCHEMY_POOL_SIZE = db_cfg["pool_size"]
    SQLALCHEMY_MAX_OVERFLOW = db_cfg["max_overflow"]
    SQLALCHEMY_POOL_RECYCLE = db_cfg["pool_recycle"]
    SQLALCHEMY_POOL_TIMEOUT = db_cfg["pool_timeout"]
    SQLALCHEMY_TRACK_MODIFICATIONS = db_cfg["modify"]
    # 读写分离
    write_cfg = cfg["base"]["writeDb"]
    SQLALCHEMY_BINDS = {
        "read": "oracle://{username}:{password}@{host}:{port}/{service}".format(**db_cfg),  #todo: 重复的配置
        "write": "oracle://{username}:{password}@{host}:{port}/{service}".format(**write_cfg),
    }

    # 默认日志等级
    LOG_LEVEL = logging.INFO
    LOG_PATH = os.path.abspath(cfg.get('log'))
