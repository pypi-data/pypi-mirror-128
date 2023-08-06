# !/usr/bin/env python
# coding:utf-8

# Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.

# Based on the Apache License 2.0 open source protocol.

__author__ = 'quinn.7@foxmail.com'


from rains.common.decorator import singleton_pattern


@singleton_pattern
class CaseRecorder(object):
    """
    用例记录器

    * 该模块负责记录用例执行时产生的日志，并且暂存至下一次读取。

    """

    _record_count: int
    """ 记录计数器 """

    _record_list: list
    """ 记录列表 """

    def __init__(self):
        """
        初始化
        """
        self._record_count = 0
        self._record_list = []

    @property
    def record_count(self):
        return self._record_count

    @property
    def record_list(self):
        return self._record_list

    def write(self, record: str):
        """
        录入
        """
        self._record_list.append(f'{ self._record_count }:: { record }')
        self._record_count += 1

    def read(self) -> str:
        """
        读取

        * 读取后，缓冲器会清空所有暂存数据。

        Return:
            所有记录拼接成的字符串

        """
        return_record_str = ''
        for record in self._record_list:
            return_record_str += record
            return_record_str += '\n'

        self._record_count = 0
        self._record_list.clear()

        return return_record_str
