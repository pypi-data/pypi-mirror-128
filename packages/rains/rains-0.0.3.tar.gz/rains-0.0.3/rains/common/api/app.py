# !/usr/bin/env python
# coding:utf-8

# Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.

# Based on the Apache License 2.0 open source protocol.

__author__ = 'quinn.7@foxmail.com'


from flask import Flask
from flask import render_template

from rains.common.api.common import *

from rains.common.db.sql import Sql
from rains.common.db.database import Database


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 数据库实例
db: Database = Database()


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """
    首页模板
    """
    return render_template(r'home.html', ico='/resource/orange.ico')
