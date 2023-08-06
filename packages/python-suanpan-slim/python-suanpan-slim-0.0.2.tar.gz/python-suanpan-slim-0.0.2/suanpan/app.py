# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.stream import stream
from suanpan.utils import tools


class APP:
    def __init__(self):
        self.func = None

    def __call__(self, func):
        self.func = func

    def start(self):
        for context in stream.subscribeMessage():
            result = self.func(context)
            if result is not None:
                data = tools.formatOutput(result)
                print(data)
                stream.sendMessage(data, context)


app = APP()
