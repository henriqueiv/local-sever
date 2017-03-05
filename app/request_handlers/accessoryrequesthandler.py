from tornado import web
from app.factories.accessoryfactory import AccessoryFactory
import json
from app.request_handlers.userauthbaserequesthandler import UserAuthBaseRequestHandler

class AccessoryRequestHandler(UserAuthBaseRequestHandler):

	accessory_factory = AccessoryFactory()

	@web.asynchronous
	def get(self, *args):
		self.validate_user()
		
		self.write(json.dumps(self.accessory_factory.get_accessories_for_api()))
		self.finish()