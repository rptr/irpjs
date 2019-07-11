#!/usr/bin/python3

# server for js impress remote

import json
from collections import OrderedDict
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

class IRPApp (WebSocketApplication):
    def on_open (self):
        self.connected = False
        print("new conn")

    def on_message (self, message):

        # handshake
        if 'hello' == message:
            self.ws.send('hello')
            self.connected = True

        elif None == message:
            pass # disconnected

        else:
            print(message)
            data = json.loads(message)
            self.irp_msg(data)

    def irp_msg (self, msg):
        action = msg["action"]
        print(action)

    def on_close (self, reason):
        print("close", reason)

addr = ('0.0.0.0', 8000)
WebSocketServer(addr, Resource(OrderedDict([('/', IRPApp)]))).serve_forever()
