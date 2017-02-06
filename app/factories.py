from models import Accessory, AccessoryLog
import pymongo
from pymongo import MongoClient

class AbstractFactory(object):
	client = None
	db = None
	table = None

	def __init__(self):
		self.client = MongoClient('localhost', 27017)
		self.db = self.client['420bits']
		

class AccessoryFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.accessories

	def insert_or_update(self, accessory):
		accessory_dictionary = {"_id": accessory.id, "name": accessory.name, "type": accessory.type, "value": accessory.value}
		self.table.update({"_id": accessory.id}, accessory_dictionary,True)


class AccessoryLogFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.data_log

	def insert(self, accessory_log):
		self.table.insert_one({"timestamp": accessory_log.timestamp, "accessory": accessory_log.accessory.to_db_json()})

	def get_logs(self, from_timestamp = 0, limit = 100):
		find_object = {"timestamp": {"$gte": float(from_timestamp)}}
		logs = self.table.find(find_object).sort({"timestamp": 1})

		max_log_timestamp = 0.0
		logs_json = []
		for log in logs.limit(limit):
			log["_id"] = str(log["_id"]) 
			logs_json.append(log)
			max_log_timestamp = max(max_log_timestamp, float(log["timestamp"])

		response = { "max_log_timestamp": max_log_timestamp, "total_results": logs.count(), "logs": logs_json }
		return response