# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json


class Arg:

    def __init__(self, key, alias=None, default=None):
        self.key = key
        self.alias = alias
        self.default = default

    def getValue(self, func, value):
        return func(value) if value is not None else self.default

    def context(self, func, value):
        value = self.getValue(func, value)
        return {
            self.key: value,
            self.alias: value
        } if self.alias else {
            self.key: value
        }


class String(Arg):

    def load(self, value):
        return self.context(str, value)

    def dump(self, value):
        return self.context(str, value)


class Json(Arg):

    def load(self, value):
        return self.context(json.loads, value)

    def dump(self, value):
        return self.context(json.dumps, value)


class Int(Arg):

    def load(self, value):
        return self.context(int, value)

    def dump(self, value):
        return self.context(int, value)


class Float(Arg):

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