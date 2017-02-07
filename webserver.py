from app.accessory_manager import AccessoryManager
from app.models import SocketMessage, SocketMessageActionRead, SocketMessageActionTurnOn, SocketMessageActionTurnOff
from app.factories import AccessoryLogFactory
from tornado import websocket, web, ioloop
import json
import time
import os

cl = []

class SocketHandler(websocket.WebSocketHandler):

    accessory_manager = AccessoryManager()

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

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
            self.update_all_clients(self.accessory_manager.get_accessories_json())

            print "Turn on: " + str(socket_message.id)

        elif socket_message.action == SocketMessageActionTurnOff and socket_message.id is not None:
            self.accessory_manager.turn_off_accessory(socket_message.id)
            self.update_all_clients(self.accessory_manager.get_accessories_json())

            print "Turn off: " + str(socket_message.id)

        elif socket_message.action == SocketMessageActionRead:
            self.update_self_client(self.accessory_manager.get_accessories_json())
            print "Read"

    def update_all_clients(self, object):
        data = json.dumps(object)
        for c in cl:
            c.write_message(data)

    def update_self_client(self, object):
        data = json.dumps(object)
        self.write_message(data)



class AccessoriesHandler(web.RequestHandler):
    @web.asynchronous
    def post(self):
        pass

    @web.asynchronous
    def get(self, *args):

        limit = int(self.get_query_argument("limit", 0))
        from_timestamp = float(self.get_query_argument("from", 0))

        log_factory = AccessoryLogFactory()
        self.write(json.dumps(log_factory.get_logs_for_api(from_timestamp,limit)))
        
        self.finish()
        print "Received get request.'from' get request param value: "
        print self.get_query_argument("from")

class AccessoryLogsHandler(web.RequestHandler):
    @web.asynchronous
    def post(self):
        print "Action parameter:" + self.get_argument("action", "")

        self.write("Headers: " + str(self.request.headers.get_all()))
        self.write("{}")
        self.write("<br>")
        self.finish()
        

app = web.Application([
    (r'/ws', SocketHandler),
    (r'/accessories', AccessoriesHandler),
    (r'/accessories_log', AccessoryLogsHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
