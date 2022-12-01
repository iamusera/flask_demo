from .exception_middleware import global_exception_handler
from .record_request_middleware import record_request
from .record_response_middleware import record_response


def init_middleware(app):
    record_request(app)
    global_exception_handler(app)
    record_response(app)