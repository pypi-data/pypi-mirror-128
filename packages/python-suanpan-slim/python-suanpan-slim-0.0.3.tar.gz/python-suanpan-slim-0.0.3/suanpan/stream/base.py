# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json
import uuid
import redis
from suanpan.g import g
from suanpan.log import logger
from suanpan.base import Context


class LocalMQ:
    def __init__(self, **kwds):
        pass

    def xadd(self, *args):
        print(args)

    def xreadgroup(self, *args, **kwds):
        return None

    def xgroup_create(self, *args, **kwds):
        pass


class Stream:
    def __init__(self):
        if g.get("mqType") == "redis":
            self.client = redis.Redis(
                host=g.get("mqRedisHost"),
                port=6379,
                decode_responses=True,
                socket_keepalive=True,
                socket_connect_timeout=1,
            )
        else:
            self.client = LocalMQ()

    def generateRequestId(self):
        return uuid.uuid4().hex

    def generateMessage(self):
        message = Context(extra={}, request_id=self.generateRequestId())
        return message

    def sendMessage(self, data, message):
        output = {
            "node_id": g.nodeId,
            "request_id": message.request_id,
            "extra": message.extra,
            "success": "true",
            **data
        }
        return self.client.xadd(g.get("streamSendQueue"), output)

    def subscribeMessage(self):
        while True:
            try:
                messages = self.client.xreadgroup(
                    "default",
                    g.nodeId, {g.get("streamRecvQueue"): ">"},
                    count=1,
                    block=60000,
                    noack=False)
            except Exception as e:  # pylint: disable=broad-except
                logger.info(f"Error {e} in receiving messages. Wait 0s")
                self.client.xgroup_create(g.get("streamRecvQueue"),
                                          "default",
                                          id="0",
                                          mkstream=True)
                continue
            if messages:
                for message in messages:
                    queue, items = message
                    for item in items:
                        mid, data = item
                        self.client.xack(queue, "default", mid)
                        requestId = data["id"]
                        extra = data["extra"]
                        context = Context(extra=extra, request_id=requestId)
                        try:
                            for k, v in data.items():
                                if k.startswith("in") and k[-1].isdigit():
                                    context.update({k: v})
                            yield context
                        except Exception as e:
                            logger.info(
                                f"Receive wrong message from upstream: {str(e)}"
                            )
