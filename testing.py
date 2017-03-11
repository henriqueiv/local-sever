from app.classes.socketclientsupdater import SocketClientsUpdater
from app.models.socketmessage import SocketMessage
from tornado import websocket, web, ioloop
import json
import time
import os
import thread
import threading
import websocket as _websocket
from pprint import pprint

clients = []

raspberries = []

class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        clients.append(self)
        print "Connection open"

    def on_close(self):
        clients.remove(self)
        print "Connection close"

    def on_message(self, message):
        print "Received messaged: " + message
        try:
            message_object = json.loads(message)
            if message_object.has_key("register"):
                print "Registered"
                raspberries.append(self)
                return
        except Exception, e:
            print "Error: " + str(e)
        
        try:
            print "1"
            if self in raspberries:
                print "Is raspberry sending message: Will notify clients"
                for client in clients:
                    if client not in raspberries and self != client:
                        client.write_message(str(message))
            else:
                print "Is client sending message: Will notify rasps"
                for raspberry in raspberries:
                    try:
                        raspberry.write_message(message)
                    except Exception as e:
                        print "Error: " + str(e)
                        
                    print "Did Write Rasp: " + str(raspberry)
                

        except Exception as e:
            print "Error: " + str(e)



app = web.Application([
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(8890)
    ioloop.IOLoop.instance().start()
