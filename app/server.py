#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
- author: Lkeme
- contact: Useri@live.cn
- file: server.py
- time: 2021/2/19 11:26
- desc:
"""
import json
from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app.client import Client
from flask import Flask, abort, jsonify, request, send_from_directory

app = Flask(__name__)


def main(address="0.0.0.0", port=5000):
    http_server = WSGIServer((address, port), app)
    http_server.serve_forever()


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


if __name__ == "__main__":
    main()
