import logging
from flask import current_app
from werkzeug.exceptions import HTTPException
from application.exception import APIException, ServerError

logger = logging.getLogger('flask_log')


def global_exception_handler(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, APIException):
            return e
        if isinstance(e, HTTPException):
            logger.info(e, exc_info=True)
            code = e.code
            msg = e.description
            return APIException(code=code, msg=msg)
        else:
            if current_app.config["DEBUG"]:
                logger.error(e)
                return e
            else:
                logger.error(e, exc_info=True)
                return ServerError(msg=str(e)).get_body()
