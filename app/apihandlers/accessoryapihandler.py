from app.factories.accessoryfactory import AccessoryFactory
import json

class AccessoryAPIHandler:

	accessory_factory = AccessoryFactory()

	def get_as_objects(self):
		return self.accessory_factory.get_accessories_for_api()

	def get_as_json_string(self):
		return json.dumps(self.get_as_objects())
