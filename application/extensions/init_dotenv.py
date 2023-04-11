#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author: iamusera
    @date: 2023-03-22 15:03
    @description: 
"""
import os
from dotenv import load_dotenv

root_path = os.path.abspath(os.path.dirname('.'))
# dot_env_path = os.path.join(root_path, '.env')
flask_env_path = os.path.join(root_path, '.flaskenv')


# if os.path.exists(dot_env_path):
#     load_dotenv(dot_env_path)

def init_dotenv():
    if os.path.exists(flask_env_path):
        load_dotenv(flask_env_path)
