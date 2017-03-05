from app.models.accessorylog import AccessoryLog
from app.factories.abstractfactory import AbstractFactory
import pymongo

class AccessoryLogFactoryGetParams:
	start_timestamp = None
	end_timestamp = None
	accessory_id = None
	sort_order = 1
	order_by = "timestamp"
	limit = None

	def find_filter_object(self):
		filter_object = {}

		if self.end_timestamp is not None or self.start_timestamp is not None:
			filter_object["timestamp"] = {}

		if self.end_timestamp is not None and self.end_timestamp > 0:
			filter_object["timestamp"]["$lte"] = float(self.end_timestamp)

		if self.start_timestamp is not None:
			filter_object["timestamp"]["$gte"] = float(self.start_timestamp)

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

		max_log_timestamp = 0.0
		logs_json = []
		for log in logs:
			log["_id"] = str(log["_id"]) 
			logs_json.append(log)
			max_log_timestamp = max(max_log_timestamp, float(log["timestamp"]))


		response = {
			"max_log_timestamp": max_log_timestamp,
			"total_results": logs.count(),
			"logs": logs_json
		}

		return response