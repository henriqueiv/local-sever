from app.accessory_manager import AccessoryManager
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


        if socket_message.action == "turn_on" and socket_message.id is not None:
            deviceToTurnOn = socket_message.id
            self.accessory_manager.turn_on_accessory(deviceToTurnOn)
            self.update_all_clients(self.accessory_manager.get_accessories_json())

            print "Turn on: " + str(deviceToTurnOn)

        elif socket_message.action == "turn_off" and socket_message.id is not None:
            deviceToTurnOff = socket_message.id
            self.accessory_manager.turn_off_accessory(deviceToTurnOff)
            self.update_all_clients(self.accessory_manager.get_accessories_json())

            print "Turn off: " + str(deviceToTurnOff)

        elif socket_message.action == "read":
            self.update_self_client(self.accessory_manager.get_accessories_json())
            print "Read"

    def update_all_clients(self, object):
        data = json.dumps(object)
        for c in cl:
            c.write_message(data)

    def update_self_client(self, object):
        data = json.dumps(object)
        self.write_message(data)


class SocketMessage:
    action = None
    id = None

    def __init__(self, socket_message):
        try:
            message_object = json.loads(socket_message)

            if message_object.has_key("action"):
                self.action = message_object["action"]

            if message_object.has_key("id"):
                self.id = message_object["id"]

        except:
            print("error parsing message:" + str(message))
            return





class TimerHandler(web.RequestHandler):

    @web.asynchronous
    def post(self):
        pass

    @web.asynchronous
    def get(self, *args):
        self.finish()
        print "Received get request.'from' get request param value: "
        print self.get_query_argument("from")

app = web.Application([
    (r'/ws', SocketHandler),
    (r'/timer', TimerHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
