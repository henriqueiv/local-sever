DEV = True

from app.classes.socketclientsupdater import SocketClientsUpdater
from app.models.socketmessage import SocketMessage, SocketMessageActionRead, SocketMessageActionTurnOn, SocketMessageActionTurnOff
from tornado import websocket, web, ioloop
import json
import time
import os
import thread
import threading
import websocket as _websocket

clients_updater = SocketClientsUpdater()





remote_ws = None
local_ws = None

def on_message_remote(ws, message):
    local_ws.send(message)
    print message

def on_error_remote(ws, error):
    print error

def on_close_remote(ws):
    print "### closed remote ###"

def on_open_remote(ws):
    def run(*args):
        ws.send("{\"register\": \"aaa\"}")
    thread.start_new_thread(run, ())
    print "### opened remote ###"

def on_message_local(ws, message):
    clients_updater.update_all_clients_with_message(message)
    print message

def on_error_local(ws, error):
    print error

def on_close_local(ws):
    print "### closed local ###"

def on_open_local(ws):
    print "### opened local ###"

def run_remote():
    if remote_ws is not None:
        remote_ws.run_forever()

def run_local():
    if local_ws is not None:
        local_ws.run_forever()

_websocket.enableTrace(True)

local_ws = _websocket.WebSocketApp("ws://127.0.0.1:8888/ws",
                  on_message = on_message_local,
                  on_error = on_error_local,
                  on_close = on_close_local)
local_ws.on_open = on_open_local


wst_local = threading.Thread(target=run_local)
wst_local.daemon = True
wst_local.start()







class SocketHandler(websocket.WebSocketHandler):


    def check_origin(self, origin):
        return True

    def open(self):
        if self not in clients_updater.clients:
            clients_updater.clients.append(self)

    def on_close(self):
        if self in clients_updater.clients:
            clients_updater.clients.remove(self)

    def on_message(self, message):
        print "Received messaged: " + message
        local_ws.send(message)

        socket_message = SocketMessage(message)

        if socket_message.action is None:
            print "Error: Action property not received in message: " + message
            return

        self.dispatch(socket_message)
        

    def dispatch(self, socket_message):
        print "Received message: " + str(socket_message) 


app = web.Application([
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(8890)
    ioloop.IOLoop.instance().start()
