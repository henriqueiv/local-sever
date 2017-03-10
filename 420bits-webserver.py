DEV = True

import json
import os
from tornado import websocket, web, ioloop
import time

from app.apihandlers.socketapihandler import SocketAPIHandler
from app.classes.socketclientsupdater import SocketClientsUpdater
from app.request_handlers.accessorylogsrequesthandler import AccessoryLogsRequestHandler
from app.request_handlers.tasksrequesthandler import TasksRequestHandler
from app.request_handlers.updateclientshandler import UpdateClientsHandler
from app.request_handlers.notesrequesthandler import NotesRequestHandler
from app.request_handlers.accessoryrequesthandler import AccessoryRequestHandler
from app.request_handlers.userrequesthandler import UserRequestHandler

import websocket as _websocket
import threading
import thread

def on_message_remote(ws, message):
    try:
        print "Message: " + str(message)
        socket_api_handler.dispatch(message, ws)
        pass
    except Exception, e:
        print "error: " + str(e)
        pass

def on_error_remote(ws, error):
    def delay_and_retry():
        time.sleep(2)
        start_cloud_thread()
        
    a = threading.Thread(target=delay_and_retry)
    a.daemon = True
    a.start()

    print error

def on_close_remote(ws):
    clients_updater.remove_client(self)
    print "### closed remote ###"

def on_open_remote(ws):
    clients_updater.add_client(ws)
    def run(*args):
        ws.send("{\"register\": \"aaa\"}")
    thread.start_new_thread(run, ())
    print "### opened remote ###"

def start_cloud_thread():
    remote_ws = _websocket.WebSocketApp("ws://127.0.0.1:8890/ws",
                  on_message = on_message_remote,
                  on_error = on_error_remote,
                  on_close = on_close_remote)
    remote_ws.on_open = on_open_remote

    def retry():
        if remote_ws is not None:
            try:
                remote_ws.run_forever()
            except Exception as e:
                print "Error: " + str(e)

    wst_remote = threading.Thread(target=retry)
    wst_remote.daemon = True
    wst_remote.start()










class BitsCloudClient:

    socket_api_handler = None
    on_close = None
    on_open = None

    def __init__(self, socket_api_handler):
        self.socket_api_handler = socket_api_handler

    def reconnect(self):
        remote_ws = _websocket.WebSocketApp("ws://127.0.0.1:8890/ws",
                      on_message = self.on_message_remote,
                      on_error = self.on_error_remote,
                      on_close = self.on_close_remote)
        remote_ws.on_open = on_open_remote

        def retry():
            if remote_ws is not None:
                try:
                    remote_ws.run_forever()
                except Exception as e:
                    print "Error: " + str(e)

        wst_remote = threading.Thread(target=retry)
        wst_remote.daemon = True
        wst_remote.start()

    def on_message_remote(self, ws, message):
        try:
            self.socket_api_handler.dispatch(message, ws)
        except Exception, e:
            print "error: " + str(e)

    def on_error_remote(self, ws, error):
        def delay_and_retry():
            time.sleep(2)
            self.reconnect()
            
        a = threading.Thread(target=delay_and_retry)
        a.daemon = True
        a.start()

    def on_close_remote(self, ws):
        if self.on_close is not None:
            self.on_close(ws)

    def on_open_remote(self, ws):
        
        def run(*args):
            ws.send("{\"register\": \"aaa\"}")

        thread.start_new_thread(run, ())

        if self.on_open is not None:
            self.on_open(ws)


def update_self_client(an_object, sender):
    if clients_updater.is_client(sender):
        clients_updater.update_client(sender, an_object)

def update_all_clients(sender):
    objects = clients_updater.update_all_clients()

_websocket.enableTrace(True)
clients_updater = SocketClientsUpdater()
socket_api_handler = SocketAPIHandler()

socket_api_handler.on_read = update_self_client
socket_api_handler.on_update = update_all_clients

cloud_client = BitsCloudClient(socket_api_handler)
cloud_client.on_open = clients_updater.add_client
cloud_client.on_close = clients_updater.remove_client

class SocketHandler(websocket.WebSocketHandler):

    socket_api_handler = None

    def initialize(self, socket_api_handler):
        self.socket_api_handler = socket_api_handler
        print "initialize"

    def check_origin(self, origin):
        return True

    def open(self):
        print "Opened connection"
        clients_updater.add_client(self)

    def on_close(self):
        clients_updater.remove_client(self)

    def on_message(self, message):
        print "Received messaged: " + message
        self.socket_api_handler.dispatch(message, self)




app = web.Application([
    (r'/ws', SocketHandler, dict(socket_api_handler = socket_api_handler)),
    (r'/users', UserRequestHandler),
    (r'/tasks', TasksRequestHandler,dict(clients_updater = clients_updater)),
    (r'/notes', NotesRequestHandler,dict(clients_updater = clients_updater)),
    (r'/accessory_logs', AccessoryLogsRequestHandler),
    (r'/accessories', AccessoryRequestHandler),
    (r'/update_clients', UpdateClientsHandler, dict(clients_updater = clients_updater)),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)

    start_cloud_thread()
    ioloop.IOLoop.instance().start()
