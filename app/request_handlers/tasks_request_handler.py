import requests
import json
import time
from tornado import web, websocket
from app.request_handlers.userauthbaserequesthandler import UserAuthBaseRequestHandler
from app.factories.timertaskfactory import TimerTaskFactory, TaskFactoryGetParams
from app.classes.socketclientsupdater import SocketClientsUpdater
from app.validators import TasksDeleteRequestHandlerValidator, TasksPostRequestHandlerValidator
from app.models.timertask import TimerTask

class TasksRequestHandler(UserAuthBaseRequestHandler):
    
    tasks_factory = TimerTaskFactory()
    socket_clients = []
    clients_updater = None

    def initialize(self, clients_updater):
        self.clients_updater = clients_updater



    @web.asynchronous
    def delete(self):
        try:
            self.validate_user()

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
                    self.write(json.dumps({"errors": ["There is not any objetc with id `" + str(id) + "`"]}))
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.clients_updater.update_all_clients()
        self.finish()

    @web.asynchronous
    def get(self, *args):
        try:
            self.validate_user()

            params = TaskFactoryGetParams()
            params.accessory_id = self.get_query_argument("accessory_id", None)

            self.write(json.dumps(self.tasks_factory.get_tasks_for_api(params)))
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.finish()

    @web.asynchronous
    def post(self):
        try:
            self.validate_user()
            
            json_object = json.loads(str(self.request.body))

            task_handler_validator = TasksPostRequestHandlerValidator()
            task_handler_validator.validate(json_object)

            if task_handler_validator.has_errors():
                self.write(json.dumps({"errors": task_handler_validator.error_messages}))
            else:
                timer_task = TimerTask(json_object)
                timer_task.user_id = self.authenticated_user_id()
                timer_task.creation_date = time.time()

                timer_task.id = str(self.tasks_factory.insert(timer_task))
                self.write(json.dumps(timer_task.mongo_json_representation()))
                self.clients_updater.update_all_clients()
    
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.finish()