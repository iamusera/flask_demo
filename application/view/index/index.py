from flask import Blueprint, jsonify
import simplejson
import logging


index_bp = Blueprint('Index', __name__, url_prefix='/')
logger = logging.getLogger('flask_log')


@index_bp.route('/')
def index():
    logger.info('ab1111c')
    return jsonify({"code": 200, "msg": 'ok'})
