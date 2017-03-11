import requests
import json
from tornado import web, websocket
from app.request_handlers.userauthbaserequesthandler import UserAuthBaseRequestHandler
from app.classes.socketclientsupdater import SocketClientsUpdater
from app.factories.notefactory import NoteFactoryGetParams
from app.apihandlers.notesapihandler import NotesAPIHandler
from app.models.appapi import AppAPI

class NotesRequestHandler(UserAuthBaseRequestHandler):

    socket_clients = []
    clients_updater = None

    notes_api_handler = NotesAPIHandler()

    def initialize(self, clients_updater):
        self.clients_updater = clients_updater

    @web.asynchronous
    def delete(self):
        self.validate_user()

        response = ""
        try:
            json_object = json.loads(str(self.request.body))
            response = self.notes_api_handler.delete(json_object)

            self.clients_updater.update_all_clients()
        except Exception as e:
            response = str(AppAPI.Error([str(e)]))

        self.write(response)
        self.finish()

    @web.asynchronous
    def get(self, *args):
        self.validate_user()
        
        params = NoteFactoryGetParams()
        params.from_date = self.get_query_argument(NotesAPIHandler.Constants.FromDateParam, None)
        params.to_date = self.get_query_argument(NotesAPIHandler.Constants.ToDateParam, None)
        params.accessory_id = self.get_query_argument(NotesAPIHandler.Constants.AccessoryIDParam, None)
        response = self.notes_api_handler.get(params)

        self.write(response)
        self.finish()

    @web.asynchronous
    def post(self):
        self.validate_user()

        response = ""
        try:
            json_object = json.loads(str(self.request.body))
            json_object[NotesAPIHandler.Constants.UserIDKey] = self.authenticated_user_id()
            response = self.notes_api_handler.create(json_object)

            self.clients_updater.update_all_clients()
        except Exception as e:
            response = str(AppAPI.Error([str(e)]))

        self.write(response)
        self.finish()