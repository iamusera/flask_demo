#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2022-12-06 13:10
"""
from flask import Blueprint

from application.responses import SuccessResponse, FailureResponse
proc_bp = Blueprint('Proc', __name__, url_prefix='/proc')

@proc_bp.route('/index_quot1')
def proc_index_quot_():
    print(123)
    return SuccessResponse(data={"var": 1}).result()
