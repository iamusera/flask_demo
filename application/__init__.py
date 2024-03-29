import os

from flask import Flask

from application.configs import config
from application.extensions import init_plugs
from application.extensions.init_dotenv import init_dotenv
from application.middleware import global_exception_handler, init_middleware
from application.view import init_view
from celery_app.celery_process import init_celery, celery_app


def create_app(config_name=None):
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    init_dotenv()
    if not config_name:
        # 尝试从本地环境中读取
        config_name = os.getenv('FLASK_CONFIG', 'development')
    print(f' * env_config: {config_name}')

    # 配置
    app.config.from_object(config[config_name]())

    # 注册工具
    init_plugs(app)

    # 注册中间件
    init_middleware(app)

    # 注册路由
    init_view(app)

    # 注册celery
    init_celery(app, celery_app)

    return app


app = create_app()