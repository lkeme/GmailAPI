#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
- author: Lkeme
- contact: Useri@live.cn
- file: server.py
- time: 2021/2/19 11:26
- desc:
"""
from gevent import monkey

monkey.patch_all()
import os
import re
import json
from gevent.pywsgi import WSGIServer
from flask import Flask, abort, jsonify, request, send_from_directory
from app.client import Client
from app.config import Config
import termcolor
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)


# 处理 Flask 写日志到文件带有颜色控制符的问题
def colored(text, color=None, on_color=None, attrs=None):
    who_invoked = traceback.extract_stack()[-2][2]  # 函数调用人
    if who_invoked == 'log_request':
        # 如果是来自 Flask/werkzeug 的调用
        return text
    else:
        # 来自其他的调用正常高亮
        COLORS = termcolor.COLORS
        HIGHLIGHTS = termcolor.HIGHLIGHTS
        ATTRIBUTES = termcolor.ATTRIBUTES
        RESET = termcolor.RESET
        if os.getenv('ANSI_COLORS_DISABLED') is None:
            fmt_str = '\033[%dm%s'
            if color is not None:
                text = fmt_str % (COLORS[color], text)
            if on_color is not None:
                text = fmt_str % (HIGHLIGHTS[on_color], text)
            if attrs is not None:
                for attr in attrs:
                    text = fmt_str % (ATTRIBUTES[attr], text)
            text += RESET
        return text


@app.before_request
def process():
    config = Config()
    # 如果没开启验证，直接跳过
    if config.get('auth', 'enable'):
        token = request.args.get("token")
        # 如果不符合条件，返回40
        if token != config.get('auth', 'token'):
            abort(401)


@app.route("/")
def root():
    return "Hello World"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")


@app.route("/fetch_mail", methods=['POST'])
def fetch_mail():
    try:
        data = json.loads(request.get_data(as_text=True))
        email = data.get('email', None)
        if email is None:
            raise Exception('未匹配到有效邮箱')
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': "invalid parameter",
        })

    result = Client(email).query_mail()
    return jsonify(result)


def main(address="0.0.0.0", port=5000):
    # 日志处理
    logger = logging.getLogger('GmailAPI')
    logging.basicConfig(level=logging.INFO)  # 记录访问
    web_log_path = os.path.join(os.getcwd(), 'logs', 'web.log')
    handler = TimedRotatingFileHandler(filename=web_log_path, when='midnight',
                                       backupCount=7, encoding='utf-8')
    handler.suffix = '%Y-%m-%d.log'
    handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False  # 不在控制台上输出

    termcolor.colored = colored
    app.logger.addHandler(handler)
    # 日志处理

    http_server = WSGIServer((address, port), app, log=app.logger)
    http_server.serve_forever()


if __name__ == "__main__":
    main()
