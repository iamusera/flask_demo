#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-02-17 12:02
    @description: 宏观python状态表映射
"""
from application.extensions import db


class PythonState(db.Model):
    id = db.Column('id', db.String(64), primary_key=True)
    query_param = db.Column('query_param', db.Text)
    module = db.Column('module', db.String(64))
    err_msg = db.Column('err_msg', db.Text)
    state = db.Column('state', db.String(64))
    create_user = db.Column('create_user', db.String(64))
    query_time = db.Column('query_time', db.DateTime)
    create_date = db.Column('create_date', db.DateTime)

    __tablename__ = 'app_mac_python_state'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
