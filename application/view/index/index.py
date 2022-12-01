from flask import Blueprint
import logging


index_bp = Blueprint('Index', __name__, url_prefix='/')
logger = logging.getLogger('flask_log')


@index_bp.route('/')
def index():
    1/0
    logger.info('ab1111c')
    return 123
