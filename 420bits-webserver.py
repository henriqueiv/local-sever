from app.accessory_manager import AccessoryManager
from app.models import SocketMessage, SocketMessageActionRead, SocketMessageActionTurnOn, SocketMessageActionTurnOff
from app.factories import AccessoryLogFactory, TimerTaskFactory
from tornado import websocket, web, ioloop
import json
import time
import os

cl = []


class Validator:
    error_messages = []
    validate_fields = []
    sub_fields_map = {}

    def has_errors(self):
        return len(self.error_messages) > 0

    def validate(self, json_object, in_key = ""):
        self.error_messages = []
        for field in self.validate_fields:
            if not json_object.has_key(field):
                error_message = "`" + str(field) + "` field not sent"
                if len(in_key) > 0:
                    error_message = error_message + " in the `" + in_key + "` field"
                self.error_messages.append(error_message)
            elif self.sub_fields_map.has_key(field):
                sub_validator = self.sub_fields_map[field]
                sub_validator.validate(json_object[field], field)
                self.error_messages.extend(sub_validator.error_messages)

class TimerValidator(Validator):
    validate_fields = [
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "seconds"
    ]

class AccessoryValidator(Validator):
    validate_fields = [
        "type",
        "_id",
        "name",
        "value",
    ]

class TaskValidator(Validator):
    validate_fields = [
        "action",
        "accessory",
        "timer",
    ]

class TasksHandlerValidator(Validator):
    task_validator = TaskValidator()
    def validate(self, request_object):
        self.task_validator.validate(request_object)
        self.error_messages.extend(self.task_validator.error_messages)







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

class NotesHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        # TODO: Fetch notes
        limit = int(self.get_query_argument("limit", 0))
        from_timestamp = float(self.get_query_argument("from", 0))

        log_factory = AccessoryLogFactory()
        self.write(json.dumps(log_factory.get_logs_for_api(from_timestamp,limit)))
        
        self.finish()
        print "Received get request.'from' get request param value: "
        print self.get_query_argument("from")

    @web.asynchronous
    def post(self):
        device_client = self.request.headers.get("CLIENT")
        device = self.request.headers.get("DEVICE")
        # TODO: Validate device client

        try:
            json_object = json.loads(str(self.request.body))
            errors = []

            text = None
            accessory_log_id = None

            if not json_object.has_key("text"):
                errors.append({"message": "field 'text' not found"})
            else:
                text = json_object["text"]

            if not json_object.has_key("accessory_log_id"):
                errors.append({"message": "field 'accessory_log_id' not found"})
            else:
                accessory_log_id = json_object["accessory_log_id"]

            if text is not None and len(text) == 0:
                errors.append({"message": "field 'text' can not be empty"})

            if accessory_log_id is not None and len(accessory_log_id) == 0:
                errors.append({"message": "field 'accessory_log_id' can not be empty"})

            if len(errors) > 0:
                self.write(json.dumps({"errors": errors}))
            else:
                generated_object_id = 1
                self.write(json.dumps({"status": "created", "object":{"id": generated_object_id, "text": text}}))

        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))
            print "Error loading json: " + str(e)

        print "Device: " + str(device_client)
        self.finish()
        
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
    def get(self, *args):
        self.write(json.dumps(self.tasks_factory.get_tasks_for_api()))
        self.finish()

    @web.asynchronous
    def post(self):
        device_client = self.request.headers.get("CLIENT")
        device = self.request.headers.get("DEVICE")
        # TODO: Validate device client

        try:
            json_object = json.loads(str(self.request.body))
            
            task_handler_validator = TasksHandlerValidator()
            timer_validator = TimerValidator()

            accessory_validator = AccessoryValidator()
            accessory_validator.validate_fields = ["_id"]

            task_handler_validator.task_validator.sub_fields_map = {
                "accessory": accessory_validator,
                "timer": timer_validator
            }

            task_handler_validator.validate(json_object)

            if task_handler_validator.has_errors():
                self.write(json.dumps({"errors": task_handler_validator.error_messages}))
            else:
                generated_object_id = 1
                self.write(json.dumps({"status": "created", "object":{"id": generated_object_id, "text": text}}))
    
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))
            print "Error loading json: " + str(e)

        print "Device: " + str(device_client)
        self.finish()







app = web.Application([
    (r'/ws', SocketHandler),
    (r'/accessories_log', AccessoriesHandler),
    (r'/update_clients', UpdateClientsHandler),
    (r'/notes', NotesHandler),
    (r'/tasks', TasksHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
