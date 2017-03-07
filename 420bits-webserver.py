DEV = True

import json
import os
from tornado import websocket, web, ioloop

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

clients_updater = SocketClientsUpdater()
socket_api_handler = SocketAPIHandler()

def on_message_remote(ws, message):
    try:
        print "remote Received message: " + str(message)
        socket_api_handler.dispatch(message, True)
        pass
    except Exception, e:
        print "error: " + str(e)
        pass

def on_error_remote(ws, error):
    print error

def on_close_remote(ws):
    print "### closed remote ###"

def on_open_remote(ws):
    def run(*args):
        ws.send("{\"register\": \"aaa\"}")
    thread.start_new_thread(run, ())
    print "### opened remote ###"

def run_remote():
    if remote_ws is not None:
        remote_ws.run_forever()

_websocket.enableTrace(True)
remote_ws = _websocket.WebSocketApp("ws://127.0.0.1:8890/ws",
                  on_message = on_message_remote,
                  on_error = on_error_remote,
                  on_close = on_close_remote)
remote_ws.on_open = on_open_remote


wst_remote = threading.Thread(target=run_remote)
wst_remote.daemon = True
wst_remote.start()

class SocketHandler(websocket.WebSocketHandler):

    socket_api_handler = None

    def initialize(self, socket_api_handler):
        self.socket_api_handler = socket_api_handler
        self.socket_api_handler.on_read = self.update_self_client
        self.socket_api_handler.on_update = self.update_all_clients
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
        self.socket_api_handler.dispatch(message, False)

    def update_self_client(self, an_object, from_remote):
        if from_remote:
            remote_ws.send(json.dumps(an_object))
        else:
            clients_updater.update_client(self, an_object)

    def update_all_clients(self, from_remote):
        objects = clients_updater.update_all_clients()
        remote_ws.send(json.dumps(objects))




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
    ioloop.IOLoop.instance().start()
