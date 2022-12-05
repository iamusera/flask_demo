from flask import Blueprint, jsonify, current_app
import simplejson
import logging

from application.extensions import db


index_bp = Blueprint('Index', __name__, url_prefix='/')
logger = logging.getLogger('flask_log')


@index_bp.route('/')
def index():
    read_sql = """
    SELECT * FROM ( SELECT t.*, ROWID FROM DSS.CB_INDEX_RESULT t ) WHERE ROWNUM <= 501 """
    write_sql = """ insert into BIZ_FOF_FUND_IND_ABL_1M(TRDE_DT, FUND_CODE, DATA_DIM) values('20220101', 'abc', '1M')"""
    # 读
    s = db.session.execute(read_sql, bind=db.get_engine('read')).fetchall()
    # 写
    db.session.execute(write_sql, bind=db.get_engine('write'))
    db.session.commit()
    logger.info('ab1111c')
    return jsonify({"code": 200, "msg": 'ok'})
