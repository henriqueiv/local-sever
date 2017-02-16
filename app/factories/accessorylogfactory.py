from app.models.accessorylog import AccessoryLog
from app.factories.abstractfactory import AbstractFactory
import pymongo

class AccessoryLogFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.data_log

	def insert(self, accessory_log):
		return self.table.insert_one(accessory_log.mongo_json_representation())

	def get_logs_for_api(self, from_timestamp = 0, limit = 0):
		find_object = {"timestamp": {"$gt": float(from_timestamp)}}
		logs = self.table.find(find_object).limit(limit).sort("timestamp", 1)

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