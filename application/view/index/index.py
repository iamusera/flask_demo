import time

import numpy as np
import pandas as pd
from flask import Blueprint, jsonify
from loguru import logger
import datetime

from application.responses import SuccessResponse, FailureResponse

from pandas.api.types import is_datetime64_any_dtype

index_bp = Blueprint('Index', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    # res = """ select * from area_rate """
    # r = DB.orm_insert('area_rate', 12)
    start = '20200301'
    end = '20230228'
    interest_rate_indicator = '2692'#2692
    rollback = 12
    indicators = ["M0017126","M0001551"]
    res_table_left, res_table_right ,result_predict2,predict_history_1y = run(interest_rate_indicator, start, end, indicators,
                                                                 rollback)

    def to_json(df):
        df = df.where(df.notnull(), '')
        df['x_axis'] = df.index
        if isinstance(df['x_axis'][0], datetime.date):
            df['x_axis'] = df.x_axis.astype('datetime64[ns]').dt.strftime('%Y-%m-%d')
        return df.to_dict('list')

    try:
        # 利率预测结果
        result_predict = to_json(result_predict2)
        # 实际值VS预测值
        predict_history_1y = to_json(predict_history_1y)
        # 回归结果表展示
        regression_results_a = to_json(res_table_left)
        regression_results_b = to_json(res_table_right)

        data = [result_predict, predict_history_1y, regression_results_a, regression_results_b]
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return FailureResponse(message=f"结果处理错误: {e}").result()
    return SuccessResponse(data=data).result()


