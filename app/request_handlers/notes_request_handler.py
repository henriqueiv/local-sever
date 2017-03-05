import requests
import json
import time
from tornado import web, websocket
from app.request_handlers.userauthbaserequesthandler import UserAuthBaseRequestHandler
from app.factories.notefactory import NoteFactory, NoteFactoryGetParams
from app.factories.accessoryfactory import AccessoryFactory
from app.classes.socketclientsupdater import SocketClientsUpdater
from app.models.note import Note
from app.validators import NotesPostRequestHandlerValidator, NotesDeleteRequestHandlerValidator

class NotesRequestHandler(UserAuthBaseRequestHandler):

    note_factory = NoteFactory()
    accessory_factory = AccessoryFactory()

    socket_clients = []
    clients_updater = None

    def initialize(self, clients_updater):
        self.clients_updater = clients_updater

    @web.asynchronous
    def delete(self):
        try:
            self.validate_user()

            json_object = json.loads(str(self.request.body))
            validator = NotesDeleteRequestHandlerValidator()
            validator.validate(json_object)

            if validator.has_errors():
                self.write(json.dumps({"errors": validator.error_messages}))
            else:
                id = str(json_object["_id"])
                if self.note_factory.delete(id):
                    self.write(json.dumps({"deleted": id}))
                else:
                    self.write(json.dumps({"errors": ["There is not any objetc with id = `" + str(id) + "`"]}))
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.clients_updater.update_all_clients()
        self.finish()

    @web.asynchronous
    def get(self, *args):
        try:
            self.validate_user()
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        params = NoteFactoryGetParams()
        params.from_date = self.get_query_argument("from_date", None)
        params.to_date = self.get_query_argument("to_date", None)
        params.accessory_id = self.get_query_argument("accessory_id", None)

        self.write(json.dumps(self.note_factory.get_notes_for_api(params)))
        self.finish()

    @web.asynchronous
    def post(self):
        try:
            self.validate_user()
            json_object = json.loads(str(self.request.body))

            notes_handler_validator = NotesPostRequestHandlerValidator()
            notes_handler_validator.validate(json_object)

            if notes_handler_validator.has_errors():
                self.write(json.dumps({"errors": notes_handler_validator.error_messages}))

            else:
                note = Note(json_object)
                note.creation_date = time.time()
                note.user_id = self.authenticated_user_id()

                note.id = str(self.note_factory.insert(note))

                self.write(json.dumps(self.note_factory.get_note_for_api(note.id)))
                self.clients_updater.update_all_clients()
    
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.finish()