#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2022-12-06 13:09
"""
from application.view.proc.index_quot import proc_bp


def register_proc_views(app):
    """
    初始化蓝图
    """

    app.register_blueprint(proc_bp)
