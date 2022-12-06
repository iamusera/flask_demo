from application.view.index import register_index_views
from application.view.proc import register_proc_views


def init_view(app):
    # register_index_views(app)
    register_proc_views(app)
