#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2022-12-06 17:32
"""

from application.extensions import db
from sqlalchemy import MetaData, Table, text

import pandas as pd


class DB:
    """
    数据库类
    """
    @classmethod
    def execute_sql(cls, sql):
        """ 执行原生sql """
        with db.engine.begin() as con:
            data = con.execute(text(sql))
            if data.returns_rows:
                data = data.fetchall()
            con.commit()
        return data

    @classmethod
    def map_table(cls, table_name, con):
        """ 获取数据库的映射 """
        metadata_obj = MetaData()
        # reflect individual table
        t = Table(table_name, metadata_obj, autoload_with=con)
        return t

    @classmethod
    def orm_insert(cls, table_name, value):
        """ 映射数据库之后， 批量的插入/单条插入 """
        with db.engine.begin() as con:
            table = cls.map_table(table_name, con)
            con.execute(table.insert(), value)
            con.commit()

    @classmethod
    def pd_read_sql(cls, sql):
        """ pandas read sql """
        with db.engine.begin() as con:
            return pd.read_sql(text(sql), con)
