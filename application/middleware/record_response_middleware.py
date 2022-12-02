from __future__ import annotations
import loguru
import logging
# from loguru import logger


logger = logging.getLogger('record_response')


def record_response(app):
    @app.after_request
    def record(response):
        d = f"""
status_code: {response.status_code}
mimetype: {response.mimetype}
json: {response.get_json()}"""
        logger.info(d)
        return response
