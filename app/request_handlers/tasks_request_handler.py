import requests
import json
from tornado import web, websocket
from app.request_handlers.userauthbaserequesthandler import UserAuthBaseRequestHandler
from app.classes.socketclientsupdater import SocketClientsUpdater
from app.apihandlers.tasksapihandler import TasksAPIHandler

class TasksRequestHandler(UserAuthBaseRequestHandler):
    
    socket_clients = []
    clients_updater = None

    tasks_api_handler = TasksAPIHandler()

    def initialize(self, clients_updater):
        self.clients_updater = clients_updater

    @web.asynchronous
    def delete(self):
        self.validate_user()

        response = ""
        try:
            json_object = json.loads(str(self.request.body))
            response = self.tasks_api_handler.delete(json_object)

            self.clients_updater.update_all_clients()
        except Exception as e:
            response = json.dumps({"errors": [{"message": str(e)}]})

        self.write(response)
        self.finish()

    @web.asynchronous
    def get(self, *args):
        self.validate_user()
        response = ""
        try:
            params = TaskFactoryGetParams()
            params.accessory_id = self.get_query_argument("accessory_id", None)

            response = self.tasks_api_handler.get(params)
        except Exception as e:
            response = json.dumps({"errors": [{"message": str(e)}]})

        self.write(response)
        self.finish()

    @web.asynchronous
    def post(self):
        self.validate_user()
        response = ""
        try:
            json_object = json.loads(str(self.request.body))
            json_object["user_id"] = self.authenticated_user_id()

            response = self.tasks_api_handler.create(json_object)
            self.clients_updater.update_all_clients()
        except Exception as e:
            response = json.dumps({"errors": [{"message": str(e)}]})

        self.write(response)
        self.finish()