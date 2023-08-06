# !/usr/bin/env python
# coding:utf-8

# Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.

# Based on the Apache License 2.0 open source protocol.

__author__ = 'quinn.7@foxmail.com'


from flask import Flask
from flask import render_template

from rains.common.db.sql import Sql
from rains.common.api.common import *


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """
    首页模板
    """
    return render_template(r'home.html', ico='/resource/orange.ico')
