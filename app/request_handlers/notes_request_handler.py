import requests
import json
import time
from tornado import web, websocket
from app.factories.notefactory import NoteFactory, NoteFactoryGetParams
from app.factories.accessorynotefactory import AccessoryNoteFactory
from app.classes.socketclientsupdater import SocketClientsUpdater
from app.models.note import Note
from app.validators import NotesPostRequestHandlerValidator, NotesDeleteRequestHandlerValidator

class NotesRequestHandler(web.RequestHandler):
    accessory_note_factory = AccessoryNoteFactory()
    note_factory = NoteFactory()
    socket_clients = []
    clients_updater = None

    def initialize(self, clients_updater):
        self.clients_updater = clients_updater

    @web.asynchronous
    def delete(self):
        try:
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
        except:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.clients_updater.update_all_clients()
        self.finish()

    @web.asynchronous
    def get(self, *args):
        params = NoteFactoryGetParams()
        params.start_timestamp = self.get_query_argument("start_timestamp", None)
        params.end_timestamp = self.get_query_argument("end_timestamp", None)

        self.write(json.dumps(self.note_factory.get_notes_for_api()))
        self.finish()

    @web.asynchronous
    def post(self):
        try:
            json_object = json.loads(str(self.request.body))

            notes_handler_validator = NotesPostRequestHandlerValidator()
            notes_handler_validator.validate(json_object)

            if notes_handler_validator.has_errors():
                self.write(json.dumps({"errors": notes_handler_validator.error_messages}))
            else:
                note = Note(json_object)
                note.timestamp = time.time()

                note.id = str(self.note_factory.insert(note))
                response_object = {"note": note.mongo_json_representation()}

                if note.id is not None and json_object.has_key("accessory_id"):
                    response_object["accessory"] = self.accessory_note_factory.link_note_to_accessory(str(note.id), str(json_object["accessory_id"]))

                self.write(json.dumps(response_object))
                self.clients_updater.update_all_clients()
    
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.finish()