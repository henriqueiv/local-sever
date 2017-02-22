from tornado import web
from app.factories.accessoryfactory import AccessoryFactory
import json

class AccessoryRequestHandler(web.RequestHandler):
	@web.asynchronous
	def get(self, *args):

		factory = AccessoryFactory()

    	self.write(json.dumps(factory.get_accessories_for_api()))

        self.finish()