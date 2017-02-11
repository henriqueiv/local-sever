from models import Accessory, AccessoryLog, Timer, TimerTask
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

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
		self.table.update({"_id": accessory.id}, accessory.mongo_json_representation(),True)


class TimerTaskFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.tasks

	def insert(self, timer_task):
		to_save = timer_task.mongo_json_representation()
		if to_save.has_key("_id") and self.table.find({"_id": ObjectId(to_save["_id"])}).count > 0:
			self.table.update(to_save,{"upsert": False})
			return to_save["_id"]
		else :
			to_save.pop("_id",None)
			return str(self.table.insert(to_save))

	def delete(self, task_id):
		result = self.table.delete_many({"_id": ObjectId(task_id)})
		return result.deleted_count > 0

	def get_tasks(self):
		db_tasks = self.table.find({"timer": {"$exists": True}})
		tasks = []
		for db_task in db_tasks:
			task = TimerTask(db_task)
			tasks.append(task)

		return tasks

	def get_tasks_for_api(self):
		find_object = {}
		tasks = self.table.find(find_object)

		tasks_json = []
		for task in tasks:
			task["_id"] = str(task["_id"])
			tasks_json.append(task)

		response = {
			"tasks": tasks_json
		}

		return response

class AccessoryLogFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.data_log

	def insert(self, accessory_log):
		return self.table.insert_one(accessory_log.mongo_json_representation())

	def get_logs_for_api(self, from_timestamp = 0, limit = 100):
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
			"logs": logs
		}

		return response