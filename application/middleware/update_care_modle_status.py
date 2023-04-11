#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-02-17 11:12
    @description: 
"""

import functools
from flask import request


def update_modle_stat(func):
    @functools.wraps(func)
    def clock(*args, **kwargs):
        
        result = func(*args, **kwargs)
        return result

    return clock

