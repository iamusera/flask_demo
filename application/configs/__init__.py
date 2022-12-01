from application.configs.dev_config import DevelopmentConfig
from application.configs.prod_config import ProductionConfig
from application.configs.test_config import TestConfig

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}
