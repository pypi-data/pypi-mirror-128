# !/usr/bin/env python
# coding:utf-8

# Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.

# Based on the Apache License 2.0 open source protocol.

__author__ = 'quinn.7@foxmail.com'


import traceback

from flask import jsonify
from flask import request

from rains.common.db.database import Database


# 数据库实例
DB: Database = Database()


def get_request_parameters(*paras):
    """
    解析请求参数

    * 解析请求接口时携带的参数。

    Args:
        paras (): 需要解析的参数名称列表

    Return:
        dict

    """

    try:
        # 判断用户请求模式
        request_handle = request.args
        if request.method == 'POST':
            request_handle = request.form

        # 获取请求参数
        return_para_dict = {}
        for para_name in paras:
            para_value = request_handle.get(para_name)
            return_para_dict.update({para_name: para_value})

        return return_para_dict

    except BaseException as e:
        raise Exception(f"解析请求参数时发生了异常:: { e }")


def successful(return_paras: dict or None):
    """
    请求成功的返回参数

    Args:
        return_paras (dict or None): 返回数据字典

    Return:
        dict

    """

    try:
        base_return = {
            'code': 200,
            'message': '请求成功',
            'data': {}
        }

        if return_paras:
            base_return['data'] = return_paras

        return jsonify(base_return)

    except Exception as e:
        raise Exception(f"API返回数据时发生了异常:: { e }")


def unsuccessful(err_message: str):
    """
    请求失败的返回参数

    Args:
        err_message (str): 返回的错误信息

    Return:
        dict

    """

    try:
        base_return = {
            'code': 500,
            'message': '请求失败',
            'err': err_message
        }

        return jsonify(base_return)

    except Exception as e:
        raise Exception(f"API返回数据时发生了异常:: { e }")
