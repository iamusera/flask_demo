import os
from flask import Flask

from app.configs import dev_config, config
from app.extensions import init_plugs
from app.view import init_view


def create_app(config_name=None):
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    if not config_name:
        # 尝试从本地环境中读取
        config_name = os.getenv('FLASK_CONFIG', 'development')
    print(f' * env_config: {config_name}')
    # 配置
    app.config.from_object(config[config_name])

    # 注册工具
    init_plugs(app)

    # 注册路由
    init_view(app)

    return app
