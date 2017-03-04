import requests
import json
import time
from tornado import web, websocket
from app.factories.userfactory import UserFactory
from app.models.user import User

from app.validators import UserPostRequestHandlerValidator, UserDeleteRequestHandlerValidator

class UserRequestHandler(web.RequestHandler):

    user_factory = UserFactory()

    @web.asynchronous
    def get(self, *args):
        self.write(json.dumps(self.user_factory.get_users_for_api()))
        self.finish()

    @web.asynchronous
    def delete(self):
        try:
            json_object = json.loads(str(self.request.body))
            validator = UserDeleteRequestHandlerValidator()
            validator.validate(json_object)

            if validator.has_errors():
                self.write(json.dumps({"errors": validator.error_messages}))
            else:
                id = str(json_object["_id"])
                if self.user_factory.delete(id):
                    self.write(json.dumps({"deleted": id}))
                else:
                    self.write(json.dumps({"errors": ["There is not any object with id = `" + str(id) + "`"]}))
        except:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.finish()

    @web.asynchronous
    def post(self):
        try:
            json_object = json.loads(str(self.request.body))

            post_handler_validator = UserPostRequestHandlerValidator()
            post_handler_validator.validate(json_object)

            if post_handler_validator.has_errors():
                self.write(json.dumps({"errors": post_handler_validator.error_messages}))

            else:
                user = User(json_object)
                user.id = str(self.user_factory.insert(user))

                self.write(json.dumps({"user": user.to_json()}))
    
        except Exception as e:
            self.write(json.dumps({"errors": [{"message": str(e)}]}))

        self.finish()