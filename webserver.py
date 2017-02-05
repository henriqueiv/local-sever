from tornado import websocket, web, ioloop
import json
import time
import os
import smbus
import pymongo
from pymongo import MongoClient

from app.accessory_manager import AccessoryManager

cl = []
bus = smbus.SMBus(1)
address = 0x04

client = MongoClient('localhost', 27017)
db = client['420bits']
data_log = db.data_log

def StringToBytes(val):
  retVal = []
  for c in val:
    retVal.append(ord(c))
  return retVal

def readBus():
  data = ""
  for i in range(0, 1):
          data += chr(bus.read_byte(address));
  return data

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

    def update_all_clients():
        data = json.dumps(self.accessory_manager.get_accessories_json())
        for c in cl:
            c.write_message(data)

    def update_self_client():
        print "1"
        data = json.dumps(self.accessory_manager.get_accessories_json())
        print "2"
        self.write_message()
        print "3"

    def on_message(self, message):
        print "Received messaged: " + message

        try:
            receivedObject = json.loads(message)
            if not receivedObject.has_key("action"):
                print "Key action not found"
                return

            action = receivedObject["action"]

            if action == "turn_on":
                deviceToTurnOn = receivedObject["id"]
                self.accessory_manager.turn_on_accessory(deviceToTurnOn)
                self.update_all_clients()

                print "Turn on: " + str(deviceToTurnOn)

            elif action == "turn_off":
                deviceToTurnOff = receivedObject["id"]
                self.accessory_manager.turn_off_accessory(deviceToTurnOff)
                self.update_all_clients()

                print "Turn off: " + str(deviceToTurnOff)

            elif action == "read":
                self.update_self_client()
                print "Read"

        except:
            print("error parsing message:" + str(message))


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
