#!/usr/bin/python3

# server for js impress remote

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
from collections import OrderedDict

class IRPApp (WebSocketApplication):
    def on_open (self):
        print("new conn")

    def on_message (self, message):
        print("msg", message)

    def on_close (self, reason):
        print("close", reason)

addr = ('', 8000)
WebSocketServer(addr, Resource(OrderedDict([('/', IRPApp)]))).serve_forever()
