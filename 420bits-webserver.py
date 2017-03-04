DEV = True
print "-------------"
#import os 
#dir_path = os.path.dirname(os.path.realpath(__file__))
#print dir_path

from app.classes.socketclientsupdater import SocketClientsUpdater
from app.managers.accessorymanager import AccessoryManager
from app.models.socketmessage import SocketMessage, SocketMessageActionRead, SocketMessageActionTurnOn, SocketMessageActionTurnOff
from tornado import websocket, web, ioloop
from app.request_handlers.accessorylogsrequesthandler import AccessoryLogsRequestHandler
from app.request_handlers.tasks_request_handler import TasksRequestHandler
from app.request_handlers.updateclientshandler import UpdateClientsHandler
from app.request_handlers.notes_request_handler import NotesRequestHandler
from app.request_handlers.accessoryrequesthandler import AccessoryRequestHandler
import json
import time
import os

clients_updater = SocketClientsUpdater()

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
            clients_updater.update_all_clients()

            print "Turn on: " + str(socket_message.id)

        elif socket_message.action == SocketMessageActionTurnOff and socket_message.id is not None:
            self.accessory_manager.turn_off_accessory(socket_message.id)
            clients_updater.update_all_clients()

            print "Turn off: " + str(socket_message.id)

        elif socket_message.action == SocketMessageActionRead:
            self.update_self_client(self.accessory_manager.get_accessories_json())
            print "Read"

    def update_self_client(self, object):
        data = json.dumps(object)
        self.write_message(data)




app = web.Application([
    (r'/ws', SocketHandler),
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
