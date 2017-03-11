from tornado import web, websocket
from app.factories.userfactory import UserFactory
from app.models.appapi import AppAPI

class UserAuthBaseRequestHandler(web.RequestHandler):
    user_factory = UserFactory()

    def validate_user(self):
    	try:
        	user_id = self.request.headers["Userid"] if self.request.headers.has_key("Userid") else None
        	self.user_factory.validate_user_with_id(user_id)
        except Exception as e:
            response = str(AppAPI.Error([str(e)]))
            self.write(response)
            self.finish()

    def authenticated_user_id(self):
    	return self.request.headers["Userid"] if self.request.headers.has_key("Userid") else None