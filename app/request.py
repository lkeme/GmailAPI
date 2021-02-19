#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
- author: Lkeme
- contact: Useri@live.cn
- file: http.py
- time: 2021/2/19 11:35
- desc:
"""

import socks
import requests
import httplib2
from app.utlis import Singleton
from app.config import Config


class Request(Singleton):

    def __init__(self):
        self.config = Config()

    @staticmethod
    def _assemble_httplib2(proxy_type, host, port):
        if proxy_type == 'socks5':
            return httplib2.ProxyInfo(socks.PROXY_TYPE_SOCKS5, host, port)
        if proxy_type == 'http':
            return httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, host, port)
        return None

    @staticmethod
    def _assemble_requests(proxy_type, host, port):
        if proxy_type == 'socks5':
            return {
                'http': f'socks5://{host}:{port}',
                'https': f'socks5://{host}:{port}'
            }
        if proxy_type == 'http':
            return {
                'http': f'http://{host}:{port}',
                'https': f'https://{host}:{port}'
            }
        return None

    def switch_type(self, call):
        if not self.config.get('proxy', 'enable'):
            return None
        # 目前只支持socks5 or http
        proxy_type = self.config.get('proxy', 'type')
        proxy_host = self.config.get('proxy', 'host')
        proxy_port = self.config.get('proxy', 'port')
        return call(proxy_type, proxy_host, proxy_port)

    # 初始化httplib2.Http()
    def init_httplib2(self):
        # httplib2.debuglevel = 4
        # socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, "", 1080)
        # socks.wrapmodule(httplib2)
        proxy_info = self.switch_type(self._assemble_httplib2)
        return httplib2.Http(proxy_info=proxy_info)

    # 初始化requests.Session()
    def init_requests(self):
        session = requests.Session()
        proxies = self.switch_type(self._assemble_requests)
        session.proxies = proxies
        return session


if __name__ == '__main__':
    r = Request()
    print(r.init_httplib2().proxy_info)
    print(r.init_requests().proxies)
