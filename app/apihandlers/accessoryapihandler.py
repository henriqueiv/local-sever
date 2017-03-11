from app.factories.accessoryfactory import AccessoryFactory
import json

class AccessoryAPIHandler:

	class Constants:
		FromDateParam = "from_date"
		ToDateParam = "to_date"
		AccessoryIDParam = "accessory_id"
		LimitParam = "limit"
		StateParam = "state"
		OnValue = "on"
		OffValue = "off"

	accessory_factory = AccessoryFactory()

	def get_as_objects(self):
		return self.accessory_factory.get_accessories_for_api()

	def get_as_json_string(self):
		return json.dumps(self.get_as_objects())
