from  app.models.mongodbmodel import MongoDBModel
from app.models.timer import Timer
from app.models.accessory import Accessory

TaskActionTurnOn = "turn_on"
TaskActionTurnOff = "turn_off"

class TimerTask(MongoDBModel):
	id = None
	timer = None
	action = None
	accessory_id = None
	creation_date = None
	name = None
	user_id = None

	def __init__(self, json_object):
		if json_object.has_key("_id"):
			self.id = json_object["_id"]

		self.action = json_object["action"] if json_object.has_key("action") else None
		self.name = json_object["name"] if json_object.has_key("name") else None
		self.creation_date = json_object["creation_date"] if json_object.has_key("creation_date") else None

		if json_object.has_key("user_id"):
			self.user_id = json_object["user_id"]

		if json_object.has_key("accessory_id"):
			self.accessory_id = json_object["accessory_id"]

		if json_object.has_key("timer"):
			self.timer = Timer(json_object["timer"])

	def can_execute(self):
		return self.timer.is_on_time() or self.timer.is_late()

	def mongo_json_representation(self):
		object = {"creation_date": self.creation_date, "action": self.action, "name": self.name}

		if self.accessory_id is not None:
			object["accessory_id"] = self.accessory_id

		if self.user_id is not None:
			object["user_id"] = self.user_id

		if self.id is not None:
			object["_id"] = self.id
		
		if self.timer is not None:
			object["timer"] = self.timer.to_json()
		return object

	def to_json(self):
		json_object = self.mongo_json_representation()
		print json_object
		if json_object.has_key("_id"):
			json_object["_id"] = str(json_object["_id"])

		if json_object.has_key("user_id"):
			json_object["user_id"] = str(json_object["user_id"])

		if json_object.has_key("accessory_id"):
			json_object["accessory_id"] = str(json_object["accessory_id"])

		return json_object