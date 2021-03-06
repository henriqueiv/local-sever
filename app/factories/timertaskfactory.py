from app.factories.accessoryfactory import AccessoryFactory
from app.factories.userfactory import UserFactory
from app.models.accessory import Accessory
from app.models.timertask import TimerTask, TaskActionTurnOn, TaskActionTurnOff
from app.factories.abstractfactory import AbstractFactory
from bson.objectid import ObjectId
import pymongo
import time


class TaskFactoryGetParams:
	accessory_id = None
	sort_order = 1
	order_by = "creation_date"
	limit = None

	def find_filter_object(self):
		filter_object = {}
		if self.accessory_id is not None:
			filter_object["accessory_id"] = str(self.accessory_id)
		return filter_object

class TimerTaskFactory(AbstractFactory):

	accessory_factory = AccessoryFactory()
	user_factory = UserFactory()

	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.task

	def insert(self, timer_task):
		if timer_task.action is not None and not timer_task.action in [TaskActionTurnOn, TaskActionTurnOff]:
			raise Exception("action `" + str(timer_task.action) + "` is not valid")

		timer_task.user_id = ObjectId(str(timer_task.user_id))
		self.user_factory.validate_user_with_id(timer_task.user_id)

		if timer_task.accessory_id is not None:
			self.accessory_factory.validate_accessory_with_id(timer_task.accessory_id)

		object_id = None
		to_save = timer_task.mongo_json_representation()
		if to_save.has_key("_id"):
			object_id = ObjectId(str(to_save["_id"]))
			to_save.pop("_id", None)

		if object_id is not None and self.table.find({"_id": object_id}).count() > 0:
			self.table.update({"_id": object_id}, to_save, True)
			return object_id
		else:
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

	def get_tasks_for_api(self, params = TaskFactoryGetParams()):
		tasks = self.table.find(params.find_filter_object()).sort(params.order_by, params.sort_order)

		tasks_json = []
		for task in tasks:
			tasks_json.append(TimerTask(task).to_json())

		response = {
			"tasks": tasks_json
		}

		return response