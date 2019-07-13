#!/usr/bin/python3

# server for js impress remote

import json
from collections import OrderedDict
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

import sys
sys.path.append('../libresign')
import unoremote

# TODO create some interface(?) in unoremote.py to inherit from
class Libo (unoremote.LiboListener):
    # TODO we need number of slides and current slide number
    def on_slideshow_started (self):
        print("started")

    def on_slideshow_ended (self):
        print("finished")

control = Libo()
uno = unoremote.UNOClient(control)
uno.start(True)

class IRPApp (WebSocketApplication):
    def on_open (self):
        self.connected = False
        print("new conn")

    def on_message (self, message):

        print(message)

        # handshake
        if '\"hello\"' == message:
            self.ws.send('hello')
            self.connected = True
            print('recv handshake')

        # disconnected
        elif None == message:
            pass

        else:
            data = json.loads(message)
            self.irp_msg(data)

    def irp_msg (self, msg):
        action = msg["action"]

        # TODO add exceptions for msg["xxxx"] in case there's no such key

        # NOTE it could be imagined that we'd want to process/ make checks
        #      before calling the UNOClient methods
        if 'transition_next' == action:
            uno.transition_next()

        elif 'transition_previous' == action:
            uno.transition_previous()

        elif 'goto_slide' == action:
            number = msg["number"]
            uno.goto_slide(number)

        elif 'presentation_start' == action:
            uno.presentation_start()

        elif 'presentation_stop' == action:
            uno.presentation_stop()

        elif 'presentation_blank_screen' == action:
            uno.blank_screen()

        elif 'presentation_resume' == action:
            uno.resume()

    def on_close (self, reason):
        print("close", reason)

addr = ('0.0.0.0', 8000)
WebSocketServer(addr, Resource(OrderedDict([('/', IRPApp)]))).serve_forever()
