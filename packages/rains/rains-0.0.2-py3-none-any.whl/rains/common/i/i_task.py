# !/usr/bin/env python
# coding:utf-8

# Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.

# Based on the Apache License 2.0 open source protocol.

__author__ = 'quinn.7@foxmail.com'


from abc import ABCMeta
from abc import abstractmethod


class ITask(metaclass=ABCMeta):
    """
    任务接口

    * 任务集以函数为单位描述执行用例。

    """

    @abstractmethod
    def set_class_starting(self):
        """
        设置类起点

        * 该接口将在 [ 任务类 ] 开始后执行，全程只会执行一次。

        """
        pass

    @abstractmethod
    def set_class_ending(self):
        """
        设置类终点

        * 该接口将在 [ 任务类 ] 结束后执行，全程只会执行一次。

        """
        pass

    @abstractmethod
    def set_function_starting(self):
        """
        设置函数起点

        * 该接口将在每次 [ 任务类::函数 ] 开始前执行。

        """
        pass

    @abstractmethod
    def set_function_ending(self):
        """
        设置函数终点

        * 该接口将在每次 [ 任务类::函数 ] 结束后执行。

        """
        pass
