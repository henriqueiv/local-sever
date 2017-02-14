from app.accessory_manager import AccessoryManager
from app.models import SocketMessage, SocketMessageActionRead, SocketMessageActionTurnOn, SocketMessageActionTurnOff, TimerTask
from app.factories import TimerTaskFactory
from app.validators import  TimerValidator, AccessoryValidator, TasksPostRequestHandlerValidator,TasksDeleteRequestHandlerValidator
from tornado import websocket, web, ioloop
from app.accessories_request_handler import AccessoriesRequestHandler
import json
import time
import os

cl = []


def update_all_clients(object):
    data = json.dumps(object)
    for c in cl:
        c.write_message(data)

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
            update_all_clients(self.accessory_manager.get_accessories_json())

            print "Turn on: " + str(socket_message.id)

        elif socket_message.action == SocketMessageActionTurnOff and socket_message.id is not None:
            self.accessory_manager.turn_off_accessory(socket_message.id)
            update_all_clients(self.accessory_manager.get_accessories_json())

            print "Turn off: " + str(socket_message.id)

        elif socket_message.action == SocketMessageActionRead:
            self.update_self_client(self.accessory_manager.get_accessories_json())
            print "Read"

    def update_self_client(self, object):
        data = json.dumps(object)
        self.write_message(data)

        
class UpdateClientsHandler(web.RequestHandler):

    accessory_manager = AccessoryManager()    

    @web.asynchronous
    def get(self, *args):
        accessories = self.accessory_manager.get_accessories_json()
        update_all_clients(accessories)
        self.write(json.dumps(accessories))
        self.finish()

class TasksHandler(web.RequestHandler):

    tasks_factory = TimerTaskFactory()

    @web.asynchronous
    def delete(self):
        try:
            json_object = json.loads(str(self.request.body))
            validator = TasksDeleteRequestHandlerValidator()
            validator.validate(json_object)

            if validator.has_errors():
                self.write(json.dumps({"errors": validator.error_messages}))
            else:
                id = str(json_object["_id"])
                if self.tasks_factory.delete(id):
                    self.write(json.dumps({"deleted": id}))
                else:
                    self.write(json.dumps({"errors": ["There is not any objetc with id = `" + str(id) + "`"]}))
        except:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.finish()

    @web.asynchronous
    def get(self, *args):
        self.write(json.dumps(self.tasks_factory.get_tasks_for_api()))
        self.finish()

    @web.asynchronous
    def post(self):
        try:
            json_object = json.loads(str(self.request.body))

            task_handler_validator = TasksPostRequestHandlerValidator()
            task_handler_validator.validate(json_object)

            if task_handler_validator.has_errors():
                self.write(json.dumps({"errors": task_handler_validator.error_messages}))
            else:
                timer_task = TimerTask(json_object)
                timer_task.id = str(self.tasks_factory.insert(timer_task))
                self.write(json.dumps(timer_task.mongo_json_representation()))
    
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))
            print "Error loading json: " + str(e)

        self.finish()







app = web.Application([
    (r'/ws', SocketHandler),
    (r'/accessories_log', AccessoriesRequestHandler),
    (r'/update_clients', UpdateClientsHandler),
    (r'/tasks', TasksHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
