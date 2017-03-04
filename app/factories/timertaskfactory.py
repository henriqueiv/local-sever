from app.factories.accessoryfactory import AccessoryFactory

from app.models.accessory import Accessory
from app.models.timertask import TimerTask
from app.factories.abstractfactory import AbstractFactory
from bson.objectid import ObjectId
import pymongo
import time

class TimerTaskFactory(AbstractFactory):

	accessory_factory = AccessoryFactory()

	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.task

	def insert(self, timer_task):
		accessory = self.accessory_factory.validate_accessory_with_id(timer_task.accessory_id)
		to_save = timer_task.mongo_json_representation()
		object_id = None
		if to_save.has_key("_id"):
			object_id = ObjectId(str(to_save["_id"]))
			to_save.pop("_id", None)

		if object_id is not None and self.table.find({"_id": object_id}).count() > 0:
			self.table.update({"_id": object_id}, to_save, True)
			return object_id
		else:
			to_save["creation_date"] = time.time()
			return self.table.insert(to_save)

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