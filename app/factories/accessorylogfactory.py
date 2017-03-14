from app.models.accessorylog import AccessoryLog
from app.factories.abstractfactory import AbstractFactory
import pymongo

class AccessoryLogFactoryGetParams:
	from_date = None
	to_date = None
	accessory_id = None
	sort_order = 1
	order_by = "creation_date"
	limit = None

	def find_filter_object(self):
		filter_object = {}

		if self.to_date is not None or self.from_date is not None:
			filter_object["creation_date"] = {}

		if self.to_date is not None and self.to_date > 0:
			filter_object["creation_date"]["$lte"] = float(self.to_date)

		if self.from_date is not None:
			filter_object["creation_date"]["$gte"] = float(self.from_date)

		if self.accessory_id is not None:
			filter_object["accessory_id"] = str(self.accessory_id)


		return filter_object


class AccessoryLogFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.accessory_log


	def validate_accessory_log_with_id(self, accessory_log_id):
		if accessory_log_id is None:
			raise Exception("accessory log id can not be empty")
		elif self.table.find({"_id": accessory_log_id}).count() == 0:
			raise Exception("accessory log with id `" + str(accessory_log_id) + "` does not exists")

	def insert(self, accessory_log):
		return self.table.insert_one(accessory_log.mongo_json_representation())

	def get_logs_for_api(self, params = AccessoryLogFactoryGetParams()):
		find_object = params.find_filter_object()

		logs = self.table.find(find_object).limit(params.limit).sort(params.order_by, params.sort_order)

		logs_json = []
		for mongo_log in logs:
			logs_json.append(AccessoryLog.from_mongo_object(mongo_log).to_json())


		response = {
			"logs": logs_json
		}

		return response