from app.models.timertask import TimerTask
from app.factories.abstractfactory import AbstractFactory
from bson.objectid import ObjectId
import pymongo

class TimerTaskFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.tasks

	def insert(self, timer_task):
		to_save = timer_task.mongo_json_representation()
		if to_save.has_key("_id") and self.table.find({"_id": ObjectId(to_save["_id"])}).count() > 0:
			id = ObjectId(to_save["_id"])
			to_save.pop("_id")
			print self.table.update({"_id": id}, to_save, True)

			return str(id)
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