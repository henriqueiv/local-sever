from tornado import web, websocket
from app.factories.userfactory import UserFactory

class UserAuthBaseRequestHandler(web.RequestHandler):
    user_factory = UserFactory()

    def validate_user(self):
        user_id = self.request.headers["Userid"] if self.request.headers.has_key("Userid") else None
        self.user_factory.validate_user_with_id(user_id)