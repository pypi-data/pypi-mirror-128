# coding=utf-8
from __future__ import absolute_import, print_function


def formatOutput(result):
    data = {}
    if isinstance(result, tuple):
        for i, d in enumerate(result):
            data.update({f"out{i+1}": d})
    else:
        data.update({"out1": result})
    return data
