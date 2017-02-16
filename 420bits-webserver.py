from app.classes.socketclientsupdater import SocketClientsUpdater
from app.accessory_manager import AccessoryManager
from app.models.socketmessage import SocketMessage, SocketMessageActionRead, SocketMessageActionTurnOn, SocketMessageActionTurnOff
from app.validators import  TimerValidator, AccessoryValidator
from tornado import websocket, web, ioloop
from app.request_handlers.accessories_request_handler import AccessoriesRequestHandler
from app.request_handlers.tasks_request_handler import TasksRequestHandler
from app.request_handlers.updateclientshandler import UpdateClientsHandler
import json
import time
import os


clients_updater = SocketClientsUpdater()

def update_all_clients():
    accessory_manager = AccessoryManager()
    objects = accessory_manager.get_accessories_json()
    update_all_clients_with_message(json.dumps(objects))

def update_all_clients_with_message(message):
    for c in clients_updater:
        c.write_message(message)

class SocketHandler(websocket.WebSocketHandler):

    accessory_manager = AccessoryManager()

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

        socket_message = SocketMessage(message)

        if socket_message.action is None:
            print "Error: Action property not received in message: " + message
            return

        self.dispatch(socket_message)
        

    def dispatch(self, socket_message):
        if socket_message.action == SocketMessageActionTurnOn and socket_message.id is not None:
            self.accessory_manager.turn_on_accessory(socket_message.id)
            update_all_clients()

            print "Turn on: " + str(socket_message.id)

        elif socket_message.action == SocketMessageActionTurnOff and socket_message.id is not None:
            self.accessory_manager.turn_off_accessory(socket_message.id)
            update_all_clients()

            print "Turn off: " + str(socket_message.id)

        elif socket_message.action == SocketMessageActionRead:
            self.update_self_client(self.accessory_manager.get_accessories_json())
            print "Read"

    def update_self_client(self, object):
        data = json.dumps(object)
        self.write_message(data)




app = web.Application([
    (r'/ws', SocketHandler),
    (r'/tasks', TasksRequestHandler,dict(socket_clients = clients_updater.clients)),
    (r'/accessories_log', AccessoriesRequestHandler),
    (r'/update_clients', UpdateClientsHandler, dict(clients_updater = clients_updater)),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
