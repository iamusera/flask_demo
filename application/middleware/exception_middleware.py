import logging
from flask import current_app
from werkzeug.exceptions import HTTPException
from application.exception import ApiException, ServerError

logger = logging.getLogger('flask_log')


def global_exception_handler(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        """ 全局返回json类型异常，根据异常自己配 """
        if isinstance(e, ApiException):
            return ServerError(msg=str(e))
        if isinstance(e, HTTPException):
            logger.error(e, exc_info=True)
            code = e.code
            msg = e.description
            return ApiException(code=code, msg=msg)
        else:
            if current_app.config["DEBUG"]:
                logger.error(e, exc_info=True)
                return ServerError(msg=str(e))
            else:
                logger.error(e, exc_info=True)
                return ServerError(msg=str(e))
