# !/usr/bin/env python
# coding:utf-8

# Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.

# Based on the Apache License 2.0 open source protocol.

__author__ = 'quinn.7@foxmail.com'


from rains.common.const import ConstTaskAndCaseState
from rains.common.db.const import ConstDatabaseTaskNaming
from rains.common.db.const import ConstDatabaseCaseNaming
from rains.common.db.const import ConstDatabaseTableNaming


class Sql(object):
    """
    SQL语句

    * 动态拼接 SQLite 语句。

    """

    @staticmethod
    def get_tasks_count() -> str:
        """
        查询所有任务数量
        """
        return f""" 

        SELECT COUNT(id)

        FROM { ConstDatabaseTableNaming.TASKS }

        """

    @staticmethod
    def tasks_get_item(paras: dict = None) -> str:
        """
        查询任务

        * 返回指定任务ID的任务信息。

        参数:
            * tid (int): 任务ID，不可为空

        """
        # 处理参数
        paras = _machining_parameter(paras, [ConstDatabaseCaseNaming.TID])

        return f"""

        SELECT *

        FROM { ConstDatabaseTableNaming.TASKS }

        WHERE ID = { paras[ConstDatabaseCaseNaming.TID] }

        """

    @staticmethod
    def tasks_get_all_item(paras: dict = None) -> str:
        """
        查询所有任务

        * 返回所有任务信息列表。

        参数:
            * page (int): 页数
            * number (int): 查询个数

        """
        # 处理参数
        paras = _machining_parameter(paras, [])
        # 获取数据返回量限制
        limit = _get_desc_limit_section(paras)

        return f"""

        SELECT * 
        
        FROM { ConstDatabaseTableNaming.TASKS }

        ORDER BY ID DESC 

        { limit }

        """

    @staticmethod
    def tasks_get_date_list(paras: dict = None) -> str:
        """
        查询工作日列表

        * 返回去重后的所有包含任务信息的日期列表。

        参数:
            * page (int): 页数
            * number (int): 查询个数

        """
        # 处理参数
        paras = _machining_parameter(paras, [])
        # 获取数据返回量限制
        limit = _get_desc_limit_section(paras)

        return f"""

        SELECT DISTINCT { ConstDatabaseTaskNaming.EXECUTE_DATE } 
        
        FROM { ConstDatabaseTableNaming.TASKS }
        
        ORDER BY ID DESC

        { limit }

        """

    @staticmethod
    def tasks_add(paras: dict = None) -> str:
        """
        创建任务

        * 创建任务执行信息。

        参数:
            * name (str): 任务名称，不可为空
            * remark (str): 任务备注，不可为空
            * execute_date (date): 执行日期，不可为空

        """
        # 处理参数
        paras = _machining_parameter(paras,
                                     [
                                         ConstDatabaseTaskNaming.NAME,
                                         ConstDatabaseTaskNaming.REMARK,
                                         ConstDatabaseTaskNaming.EXECUTE_DATE
                                     ])

        return f""" 

        INSERT INTO { ConstDatabaseTableNaming.TASKS } (
        
             id, 
             { ConstDatabaseTaskNaming.NAME },
             { ConstDatabaseTaskNaming.REMARK },
             { ConstDatabaseTaskNaming.EXECUTE_DATE },
             { ConstDatabaseTaskNaming.IS_COMPLETED },
             { ConstDatabaseTaskNaming.START_TIME },
             { ConstDatabaseTaskNaming.END_TIME },
             { ConstDatabaseTaskNaming.CASE_ALL },
             { ConstDatabaseTaskNaming.CASE_PASS },
             { ConstDatabaseTaskNaming.CASE_FAIL }
        )
        
        VALUES (
        
            NULL,
            '{ paras[ConstDatabaseTaskNaming.NAME] }',
            '{ paras[ConstDatabaseTaskNaming.REMARK] }',
            '{ paras[ConstDatabaseTaskNaming.EXECUTE_DATE] }',
             0, NULL, NULL, NULL, NULL, NULL
        )

        """

    @staticmethod
    def tasks_update(paras: dict = None) -> str:
        """
        更新任务

        * 更新任务信息。

        参数:
            * tid (int): 所属任务ID，不可为空
            * start_time (date): 开始时间，不可为空
            * end_time (date): 结束时间，不可为空
            * case_all (int): 所有用例数，不可为空
            * case_pass (int): 成功的用例数，不可为空
            * case_fail (int): 失败用例数量，不可为空

        """
        # 处理参数
        paras = _machining_parameter(paras,
                                     [
                                         ConstDatabaseTaskNaming.TID,
                                         ConstDatabaseTaskNaming.START_TIME,
                                         ConstDatabaseTaskNaming.END_TIME,
                                         ConstDatabaseTaskNaming.CASE_ALL,
                                         ConstDatabaseTaskNaming.CASE_PASS,
                                         ConstDatabaseTaskNaming.CASE_FAIL
                                     ])

        return f"""

        UPDATE { ConstDatabaseTableNaming.TASKS }

        SET
            is_completed = 1,
            start_time   = '{ paras[ConstDatabaseTaskNaming.START_TIME] }',
            end_time     = '{ paras[ConstDatabaseTaskNaming.END_TIME] }',
            case_all     =  { paras[ConstDatabaseTaskNaming.CASE_ALL] },
            case_pass    =  { paras[ConstDatabaseTaskNaming.CASE_PASS] },
            case_fail    =  { paras[ConstDatabaseTaskNaming.CASE_FAIL] }

        WHERE ID = { paras[ConstDatabaseTaskNaming.TID] }

        """

    @staticmethod
    def tasks_delete(paras: dict = None) -> str:
        """
        删除任务

        * 删除指定任务ID的任务信息。

        参数:
            * tid (int): 所属任务ID，不可为空

        """
        # 处理参数
        paras = _machining_parameter(paras, [ConstDatabaseTaskNaming.TID])

        return f"""

        DELETE FROM { ConstDatabaseTableNaming.TASKS }

        WHERE ID = { paras[ConstDatabaseTaskNaming.TID] }

        """

    @staticmethod
    def cases_get_count(paras: dict = None) -> str:
        """
        查询所有用例数量

        参数:
            * tid (int): 所属任务ID，不可为空

        """
        # 处理参数
        paras = _machining_parameter(paras, [ConstDatabaseTaskNaming.TID])

        return f""" 

        SELECT COUNT(id) FROM { ConstDatabaseTableNaming.CASES } 
        
        WHERE { ConstDatabaseTaskNaming.TID } = { paras[ConstDatabaseTaskNaming.TID] }

        """

    @staticmethod
    def cases_get_item(paras: dict = None) -> str:
        """
        查询用例

        * 返回指定用例ID的用例信息。

        参数:
            * cid (int): 用例ID，不可为空

        """
        # 处理参数
        paras = _machining_parameter(paras, [ConstDatabaseCaseNaming.CID])

        return f"""

        SELECT * FROM { ConstDatabaseTableNaming.CASES }

        WHERE id = { paras[ConstDatabaseCaseNaming.CID] }

        """

    @staticmethod
    def cases_get_all_item(paras: dict = None) -> str:
        """
        查询用例列表

        * 返回所有用例信息列表

        参数:
            * tid (int): 所属任务ID，不可为空
            * state (str): 状态
            * page (int): 页数
            * number (int): 查询个数

        """
        # 处理参数
        paras = _machining_parameter(paras, [ConstDatabaseCaseNaming.TID])

        if ConstDatabaseCaseNaming.STATE in paras.keys():
            state = f'{ ConstDatabaseCaseNaming.STATE } = { paras[ConstDatabaseCaseNaming.STATE] }'
        else:
            state = f'{ ConstDatabaseCaseNaming.STATE } in ("{ ConstTaskAndCaseState.BLOCK }", ' \
                    f'"{ ConstTaskAndCaseState.SUCCESSFUL }", "{ ConstTaskAndCaseState.UNSUCCESSFUL }")'

        # 获取数据返回量限制
        limit = _get_desc_limit_section(paras)

        return f"""

        SELECT * FROM { ConstDatabaseTableNaming.CASES }

        WHERE { state } AND { ConstDatabaseCaseNaming.TID } = { paras[ConstDatabaseCaseNaming.TID] }

        ORDER BY ID DESC

        { limit }

        """

    @staticmethod
    def cases_add(paras: dict = None) -> str:
        """
        创建用例

        * 创建用例执行信息。

        参数:
            * tid (int): 所属任务记录ID，不可为空
            * name (str): 用例名称，不可为空
            * remark (str): 用例备注，不可为空

        """
        # 检查参数是否缺失
        paras = _machining_parameter(paras,
                                     [
                                         ConstDatabaseCaseNaming.TID,
                                         ConstDatabaseCaseNaming.NAME,
                                         ConstDatabaseCaseNaming.REMARK
                                     ])

        return f""" 

        INSERT INTO { ConstDatabaseTableNaming.CASES } (
        
            id, 
            { ConstDatabaseCaseNaming.TID }, 
            { ConstDatabaseCaseNaming.NAME }, 
            { ConstDatabaseCaseNaming.REMARK }, 
            { ConstDatabaseCaseNaming.STATE }, 
            { ConstDatabaseCaseNaming.START_TIME }, 
            { ConstDatabaseCaseNaming.END_TIME },
            { ConstDatabaseCaseNaming.RUN_STEP }
        )

        VALUES (
        
            NULL,
            '{ paras[ConstDatabaseCaseNaming.TID] }',
            '{ paras[ConstDatabaseCaseNaming.NAME] }',
            '{ paras[ConstDatabaseCaseNaming.REMARK] }',
            '{ ConstTaskAndCaseState.BLOCK }', 
             NULL, 
             NULL,
             NULL
        )

        """

    @staticmethod
    def cases_update(paras: dict = None) -> str:
        """
        更新用例

        * 更新用例信息。

        参数:
            * cid (int): 用例ID，不可为空
            * state (str): 用例状态，不可为空
            * start_time (date): 开始时间，不可为空
            * end_time (date): 结束时间，不可为空

        """
        # 处理参数
        paras = _machining_parameter(paras,
                                     [
                                         ConstDatabaseCaseNaming.CID,
                                         ConstDatabaseCaseNaming.STATE,
                                         ConstDatabaseCaseNaming.START_TIME,
                                         ConstDatabaseCaseNaming.END_TIME,
                                         ConstDatabaseCaseNaming.RUN_STEP
                                     ])

        return f"""

        UPDATE { ConstDatabaseTableNaming.CASES }

        SET 
            { ConstDatabaseCaseNaming.STATE }      = '{ paras[ConstDatabaseCaseNaming.STATE] }',
            { ConstDatabaseCaseNaming.START_TIME } = '{ paras[ConstDatabaseCaseNaming.START_TIME] }',
            { ConstDatabaseCaseNaming.END_TIME }   = '{ paras[ConstDatabaseCaseNaming.END_TIME] }',
            { ConstDatabaseCaseNaming.RUN_STEP }   = '{ paras[ConstDatabaseCaseNaming.RUN_STEP] }'

        WHERE
            ID = { paras[ConstDatabaseCaseNaming.CID] }

        """

    @staticmethod
    def cases_delete(paras: dict = None) -> str:
        """
        删除用例

        * 删除指定用例ID的用例信息。

        参数:
            * cid (int): 用例ID，不可为空

        """
        # 检查参数是否缺失
        paras = _machining_parameter(paras, [ConstDatabaseCaseNaming.CID])

        return f"""

        DELETE FROM { ConstDatabaseTableNaming.CASES }

        WHERE ID = { paras[ConstDatabaseCaseNaming.CID] }

        """

    @staticmethod
    def cases_delete_all(paras: dict = None) -> str:
        """
        删除所有用例

        * 删除指定任务ID的所有用例信息。

        参数:
            * tid (int): 所属任务ID，不可为空

        """
        # 检查参数是否缺失
        paras = _machining_parameter(paras, [ConstDatabaseTaskNaming.TID])

        return f"""

        DELETE FROM { ConstDatabaseTableNaming.CASES }

        WHERE TID = { paras[ConstDatabaseTaskNaming.TID] }

        """


def _get_desc_limit_section(paras: dict):
    """
    获取数据返回量限制

    * 默认是获取 1 页， 20 条数据。

    """
    if 'page' not in paras.keys():
        paras['page'] = 1

    if 'number' not in paras.keys():
        paras['number'] = 20

    limit_end = paras['page'] * paras['number']
    limit_begin = limit_end - paras['number']

    return f'LIMIT { limit_begin }, { limit_end }'


def _machining_parameter(paras: dict, essential_list: list):
    """
    检查参数是否缺失
    """
    if not paras:
        paras = {}

    for essential_para in essential_list:
        if paras[essential_para] is None:
            raise ParametersAreMissingException(essential_para)

    return paras


class ParametersAreMissingException(Exception):
    """
    参数缺失错误类
    """
    def __init__(self, missing_para_key):
        Exception.__init__(self, f'SQL必要参数 { missing_para_key } 缺失!')
