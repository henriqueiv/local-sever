import requests
import json
from tornado import web, websocket
from app.apihandlers.usersapihandler import UsersAPIHandler
from app.models.appapi import AppAPI

class UserRequestHandler(web.RequestHandler):

    users_api_handler = UsersAPIHandler()


    @web.asynchronous
    def get(self, *args):
        self.write(self.users_api_handler.get())
        self.finish()

    @web.asynchronous
    def delete(self):
        response = ""
        try:
            json_object = json.loads(str(self.request_body))
            response = self.users_api_handler.delete(json_object)
        except:
            response = str(AppAPI.Error([str(e)]))

        self.write(str(response))
        self.finish()

    @web.asynchronous
    def post(self):
        response = ""
        try:
            json_object = json.loads(str(self.request.body))
            response = self.users_api_handler.create(json_object)
    
        except Exception as e:
            response = str(AppAPI.Error([str(e)]))

        self.write(response)
        self.finish()