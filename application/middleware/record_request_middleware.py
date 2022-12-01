import logging
from flask import request

logger = logging.getLogger('record_request')


def record_request(app):
    @app.before_request
    def record():
        d = f"""
******************************************
    remote_addr: {request.remote_addr}
    URL: {request.path}
    mimetype: {request.mimetype}
    method: {request.method}
    args: {dict(request.args)}
    json: {request.get_json()}
        """
        logger.info(d)
