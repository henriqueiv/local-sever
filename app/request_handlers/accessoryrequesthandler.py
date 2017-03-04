from tornado import web
from app.factories.accessoryfactory import AccessoryFactory
import json

class AccessoryRequestHandler(web.RequestHandler):

	accessory_factory = AccessoryFactory()

	@web.asynchronous
	def get(self, *args):
		self.write(json.dumps(self.accessory_factory.get_accessories_for_api()))
		self.finish()