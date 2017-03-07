from tornado import web
from app.request_handlers.userauthbaserequesthandler import UserAuthBaseRequestHandler
from app.apihandlers.accessoryapihandler import AccessoryAPIHandler

class AccessoryRequestHandler(UserAuthBaseRequestHandler):

	accessoryapihandler = AccessoryAPIHandler()	

	@web.asynchronous
	def get(self, *args):
		self.validate_user()
		
		self.write(self.accessoryapihandler.get_as_json_string())
		self.finish()