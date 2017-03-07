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

clients = []

raspberries = []

class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        clients.append(self)
        print "Connection open"

    def on_close(self):
        print "Connection close"

    def on_message(self, message):
        print "Received messaged: " + message
        try:
            message_object = json.loads(message)
            if message_object.has_key("register"):
                print "Registered"
                raspberries.append(self)
                return

            pass
        except Exception, e:
            pass
        
        try:
            if self in raspberries:
                print "Is raspberry sending message: "
                for client in clients:
                    if client not in raspberries:
                        client.write_message(str(message))
            else:
                for raspberry in raspberries:
                    raspberry.write_message(message)
        except:
            pass



app = web.Application([
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(8890)
    ioloop.IOLoop.instance().start()
