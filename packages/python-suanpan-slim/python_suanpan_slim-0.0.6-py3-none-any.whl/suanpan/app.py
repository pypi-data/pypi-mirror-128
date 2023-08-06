# coding=utf-8
from __future__ import absolute_import, print_function

import json
import base64
from suanpan.g import g
from suanpan.stream import stream
from suanpan.utils import tools
from suanpan.arguments import suanpanTypes


class APP:

    def __init__(self):
        self.func = None
        nodeinfo = self.loadNodeInfo()
        self.inputArgs = self.addArguments(
            self.parseNodeInfo("inputs", nodeinfo))
        self.outputArgs = self.addArguments(
            self.parseNodeInfo("outputs", nodeinfo))
        self.paramArgs = self.addArguments(
            self.parseNodeInfo("params", nodeinfo))
        self.paramContext = self.loadParams(g)

    def parseNodeInfo(self, type, nodeinfo):
        data = {}
        for k, v in nodeinfo[type].items():
            data.update({k: {"type": v["subtype"], "uuid": v["uuid"]}})
        return data

    def loadNodeInfo(self):
        nodeInfoBase64 = g.nodeInfo
        nodeInfoString = base64.b64decode(nodeInfoBase64).decode()
        nodeInfo = json.loads(nodeInfoString)
        return nodeInfo

    def __call__(self, func):
        self.func = func

    def start(self):
        for context in stream.subscribeMessage():
            inputContext = self.loadInputs(context)
            context.args.update({**self.paramContext, **inputContext})
            result = self.func(context)
            if result is not None:
                result = self.formatOutput(result)
                result = self.saveOutputs(result)
                stream.sendMessage(result, context)

    def addArguments(self, configs):
        arguments = {}
        for key, value in configs.items():
            arguments.update({
                key: suanpanTypes[value["type"]](key=key, alias=value["uuid"])
            })
        return arguments

    def loadParams(self, context):
        params = {}
        for k, v in context.items():
            params.update(self.paramArgs[k].load(v))
        return params

    def loadInputs(self, context):
        params = {}
        for k, v in context.items():
            if k.startswith("in") and k[-1].isdigit():
                params.update(self.paramArgs[k.replace("in",
                                                       "inputData")].load(v))
        return params

    def saveOutputs(self, context):
        params = {}
        for k, v in context.items():
            if k.startswith("out") and k[-1].isdigit():
                result = self.paramArgs[k.replace("out", "outputData")].dump(v)
                for port, value in result.items():
                    if port.startswith("out"):
                        port = port.replace(
                            "outputData",
                            "out") if port.startswith("outputData") else port
                        result[port] = value
                    else:
                        del result[port]
                params.update(result)
        return params
    
    def formatOutput(self, result):
        data = {}
        if isinstance(result, tuple):
            for i, d in enumerate(result):
                if d:
                    data.update({f"out{i+1}": d})
        else:
            data.update({"out1": result})
        return data

    def send(self, result, context):
        data = tools.formatOutput(result)
        stream.sendMessage(data, context)

    def contextGen(self):
        return stream.generateMessage()

    def sendWithoutContext(self, result):
        context = self.contextGen()
        self.send(result, context)

    def input(self, args):
        self.inputArgs.update({args.key: args})
        return self

    def param(self, args):
        self.paramArgs.update({args.key: args})
        return self

    def output(self, args):
        self.outputArgs.update({args.key: args})
        return self


app = APP()
