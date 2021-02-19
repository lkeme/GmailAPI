#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
- author: Lkeme
- contact: Useri@live.cn
- file: run.py
- time: 2021/2/18 17:23
- desc:
"""

from multiprocessing import Process
from app.utlis import printer
from app.config import Config


def main():
    config = Config()
    if config.get('server', 'enable'):
        from app import server

        address = config.get('server', 'address')
        port = config.get('server', 'port')

        printer("Server: ON")
        printer(f"URL: http://{address}:{port}/")
        Process(target=server.main, args=(address, port)).start()
    else:
        printer("Server: OFF")


if __name__ == "__main__":
    main()
