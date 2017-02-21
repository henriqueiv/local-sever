import requests
import json
from tornado import web, websocket
from app.factories.notefactory import NoteFactory, NoteFactoryGetParams
from app.classes.socketclientsupdater import SocketClientsUpdater
from app.models.note import Note

class NotesRequestHandler(web.RequestHandler):

    note_factory = NoteFactory()
    socket_clients = []
    clients_updater = None

    def initialize(self, clients_updater):
        self.clients_updater = clients_updater

    @web.asynchronous
    def delete(self):
        # try:
        #     json_object = json.loads(str(self.request.body))
        #     validator = TasksDeleteRequestHandlerValidator()
        #     validator.validate(json_object)

        #     if validator.has_errors():
        #         self.write(json.dumps({"errors": validator.error_messages}))
        #     else:
        #         id = str(json_object["_id"])
        #         if self.tasks_factory.delete(id):
        #             self.write(json.dumps({"deleted": id}))
        #         else:
        #             self.write(json.dumps({"errors": ["There is not any objetc with id = `" + str(id) + "`"]}))
        # except:
        #     self.write(json.dumps({"errors": [{"message": str(e)}]}))

        # self.clients_updater.update_all_clients()
        # self.finish()
        pass

    @web.asynchronous
    def get(self, *args):
        params = NoteFactoryGetParams()
        params.start_timestamp = self.get_query_argument("start_timestamp", None)
        params.end_timestamp = self.get_query_argument("end_timestamp", None)

        self.write(json.dumps(self.note_factory.get_notes_for_api()))
        self.finish()

    @web.asynchronous
    def post(self):
        pass
        # try:
        #     json_object = json.loads(str(self.request.body))

        #     task_handler_validator = TasksPostRequestHandlerValidator()
        #     task_handler_validator.validate(json_object)

        #     if task_handler_validator.has_errors():
        #         self.write(json.dumps({"errors": task_handler_validator.error_messages}))
        #     else:
        #         timer_task = TimerTask(json_object)
        #         timer_task.id = str(self.tasks_factory.insert(timer_task))
        #         self.write(json.dumps(timer_task.mongo_json_representation()))
        #         self.clients_updater.update_all_clients()
    
        # except Exception as e:
        #     self.write(json.dumps({"errors": [{"message": str(e)}]}))

        # self.finish()