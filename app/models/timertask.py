from  app.models.mongodbmodel import MongoDBModel
from app.models.timer import Timer
from app.models.accessory import Accessory

TaskActionTurnOn = "turn_on"
TaskActionTurnOff = "turn_off"

class TimerTask(MongoDBModel):
	id = None
	timer = None
	action = None
	accessory = None
	status = None
	creation_date = None
	name = None

	def __init__(self, json_object):
		if json_object.has_key("_id"):
			self.id = json_object["_id"]

		self.action = json_object["action"] if json_object.has_key("action") else None
		self.status = json_object["status"] if json_object.has_key("status") else None
		self.name = json_object["name"] if json_object.has_key("name") else None
		self.creation_date = json_object["creation_date"] if json_object.has_key("creation_date") else None

		if json_object.has_key("accessory"):
			accessory = json_object["accessory"]
			id = accessory["_id"] if accessory.has_key("_id") else None
			type = accessory["type"] if accessory.has_key("type") else None
			name = accessory["name"] if accessory.has_key("name") else None
			value = accessory["value"] if accessory.has_key("value") else None

			self.accessory = Accessory(name, id, type, value)

		if json_object.has_key("timer"):
			self.timer = Timer(json_object["timer"])

	def can_execute(self):
		return self.timer.is_on_time() or self.timer.is_late()

	def mongo_json_representation(self):
		accessory = self.accessory.mongo_json_representation() if self.accessory is not None else {}
		object = {"status": self.status, "creation_date": self.creation_date, "action": self.action, "accessory": accessory, "name": self.name}
		if self.id is not None:
			object["_id"] = str(self.id)
		
		if self.timer is not None:
			object["timer"] = self.timer.to_json()
		return object