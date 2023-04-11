from .exception_middleware import global_exception_handler


def init_middleware(app):
    global_exception_handler(app)