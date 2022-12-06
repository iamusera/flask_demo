#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2022-12-06 13:18
"""
import typing as t
from flask import jsonify


class BaseResponse:
    code = None
    data = []
    message = ""

    def __init__(self,
                code=None,
                data=None,
                message=None,
                ):
        self.result_dic = dict()
        self.result_dic["message"] = self.message if message is None else message
        self.result_dic["data"] = self.data if data is None else data
        self.result_dic["code"] = self.code if data is None else code

    def result(self):
        return jsonify(self.result_dic)


class SuccessResponse(BaseResponse):
    """
    操作成功返回结果类
    """

    code = 200
    data = []
    message = "success"


class FailureResponse(BaseResponse):
    """
    操作失败返回结果类
    """

    code = 500
    data = []
    message = "exception"
