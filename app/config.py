#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
- author: Lkeme
- contact: Useri@live.cn
- file: config.py
- time: 2021/2/19 11:29
- desc:
"""
import os
import sys
import chardet
import toml
from app.utlis import Singleton
from app.utlis import printer


class Config(Singleton):
    config = None

    def __init__(self):
        self.root_path = f'{os.getcwd()}/conf/'
        self.load_config()

    def load_config(self):
        cf = sys.argv[1] if len(sys.argv) > 1 else "config.toml"
        cf = f'{self.root_path}{cf}'
        try:
            with open(cf, 'r', encoding=self.detect_charset(cf)) as f:
                self.config = toml.load(f)
        except Exception as e:
            printer(f'Error loading configuration file {e}')
            exit()

    @staticmethod
    def detect_charset(file, fallback="utf-8"):
        with open(file, "rb") as f:
            detector = chardet.UniversalDetector()
            for line in f.readlines():
                detector.feed(line)
                if detector.done:
                    return detector.result['encoding']
        return fallback

    def get(self, section, key):
        return self.config[section][key]

    def set(self, section, key, value):
        self.config[section][key] = value
