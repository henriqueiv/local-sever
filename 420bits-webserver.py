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

clients_updater = SocketClientsUpdater()

class SocketHandler(websocket.WebSocketHandler):

    socket_api_handler = SocketAPIHandler()

    def initialize(self):
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
        self.socket_api_handler.dispatch(message)

    def update_self_client(self, an_object):
        clients_updater.update_client(self, an_object)

    def update_all_clients(self):
        clients_updater.update_all_clients()




app = web.Application([
    (r'/ws', SocketHandler),
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
