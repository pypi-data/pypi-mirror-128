# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json


class Arg:

    def __init__(self, key, alias=None, default=None):
        self.key = key
        self.alias = alias
        self.default = default

    def getValue(self, value):
        return value if value else self.default

    def context(self, func, value):
        value = self.getValue(value)
        return {
            self.key: func(value),
            self.alias: func(value)
        } if self.alias else {
            self.key: func(value)
        }


class String(Arg):

    def load(self, value):
        return self.context(str, value)

    def dump(self, value):
        return self.context(str, value)


class Json:

    def load(self, value):
        return self.context(json.loads, value)

    def dump(self, value):
        return self.context(json.dumps, value)

class Int:

    def load(self, value):
        return self.context(int, value)

    def dump(self, value):
        return self.context(int, value)


class Float:

    def load(self, value):
        return self.context(float, value)

    def dump(self, value):
        return self.context(float, value)


# class Csv:

#     def __init__(self, key, alias=None, default=None):
#         self.key = key
#         self.alias = alias
#         self.default = default

#     def load(self, value):
#         return float(value)

#     def dump(self, value):
#         return float(value)