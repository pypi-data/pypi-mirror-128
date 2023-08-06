# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json


class String:

    def __init__(self, key, alias=None, default=None):
        self.key = key
        self.alias = alias
        self.default = default

    def load(self, value):
        return {self.key: str(value), self.alias: str(value)}

    def dump(self, value):
        return {self.key: str(value), self.alias: str(value)}


class Json:

    def __init__(self, key, alias=None, default=None):
        self.key = key
        self.alias = alias
        self.default = default

    def load(self, value):
        return {self.key: json.loads(value), self.alias: json.loads(value)}

    def dump(self, value):
        return {self.key: json.dumps(value), self.alias: json.dumps(value)}


class Int:

    def __init__(self, key, alias=None, default=None):
        self.key = key
        self.alias = alias
        self.default = default

    def load(self, value):
        return {self.key: int(value), self.alias: int(value)}

    def dump(self, value):
        return {self.key: int(value), self.alias: int(value)}


class Float:

    def __init__(self, key, alias=None, default=None):
        self.key = key
        self.alias = alias
        self.default = default

    def load(self, value):
        return {self.key: float(value), self.alias: float(value)}

    def dump(self, value):
        return {self.key: float(value), self.alias: float(value)}


# class Csv:

#     def __init__(self, key, alias=None, default=None):
#         self.key = key
#         self.alias = alias
#         self.default = default

#     def load(self, value):
#         return float(value)

#     def dump(self, value):
#         return float(value)