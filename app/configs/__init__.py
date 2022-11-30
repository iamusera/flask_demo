from app.configs.dev_config import DevelopmentConfig
from app.configs.prod_config import ProductionConfig
from app.configs.test_config import TestConfig

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}
