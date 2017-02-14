from tornado import web, websocket
from app.factories import TimerTaskFactory
import json
from app.validators import TasksDeleteRequestHandlerValidator, TasksPostRequestHandlerValidator
from app.models import TimerTask
import requests

class TasksRequestHandler(web.RequestHandler):

    tasks_factory = TimerTaskFactory()
    socket_clients = []

    def initialize(self, socket_clients):
        self.socket_clients = socket_clients

    def update_socket_clients(self):
        try:
            print "Clients: " + str(self.socket_clients)
            tasks = self.tasks_factory.get_tasks_for_api()
            print "Tasks: " + str(tasks)
            json = json.dumps(self.tasks_factory.get_tasks_for_api())
            print "JSON: " + str(json)
            for c in self.socket_clients:
                print "Will write in client: " + str(c)
                c.write_message()
        except:
            print("Error updating socket_clients:" + str(self.socket_clients))

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

        self.update_socket_clients()
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
                self.update_socket_clients()
    
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))
            print "Error loading json: " + str(e)

        self.finish()