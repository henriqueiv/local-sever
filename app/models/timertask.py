from  app.models.mongodbmodel import MongoDBModel
from app.models.timer import Timer
from app.models.accessory import Accessory
from bson.objectid import ObjectId

TaskActionTurnOn = "turn_on"
TaskActionTurnOff = "turn_off"

class TimerTask(MongoDBModel):

	class JSONField:
		ID = "_id"
		Name = "name"
		Action = "action"
		CreationDate = "creation_date"
		UserID = "user_id"
		AccessoryID = "accessory_id"
		Timer = "timer"

	class MongoDBFields:
		ID = "_id"
		Name = "name"
		Action = "action"
		CreationDate = "creation_date"
		UserID = "user_id"
		AccessoryID = "accessory_id"
		Timer = "timer"


	id = None
	timer = None
	action = None
	accessory_id = None
	creation_date = None
	name = None
	user_id = None

	def __init__(self, json_object):
		if json_object.has_key(TimerTask.JSONField.ID):
			self.id = ObjectId(str(json_object[TimerTask.JSONField.ID]))

		self.action = json_object[TimerTask.JSONField.Action] if json_object.has_key(TimerTask.JSONField.Action) else None
		self.name = json_object[TimerTask.JSONField.Name] if json_object.has_key(TimerTask.JSONField.Name) else None
		self.creation_date = json_object[TimerTask.JSONField.CreationDate] if json_object.has_key(TimerTask.JSONField.CreationDate) else None

		if json_object.has_key(TimerTask.JSONField.UserID):
			self.user_id = json_object[TimerTask.JSONField.UserID]

		if json_object.has_key(TimerTask.JSONField.AccessoryID):
			self.accessory_id = json_object[TimerTask.JSONField.AccessoryID]

		if json_object.has_key(TimerTask.JSONField.Timer):
			self.timer = Timer(json_object[TimerTask.JSONField.Timer])

	def can_execute(self):
		return self.timer.is_on_time() or self.timer.is_late()

	def mongo_json_representation(self):
		object = {TimerTask.MongoDBFields.CreationDate: self.creation_date, TimerTask.MongoDBFields.Action: self.action, TimerTask.MongoDBFields.Name: self.name}

		if self.accessory_id is not None:
			object[TimerTask.MongoDBFields.AccessoryID] = self.accessory_id

		if self.user_id is not None:
			object[TimerTask.MongoDBFields.UserID] = self.user_id

		if self.id is not None:
			object[TimerTask.MongoDBFields.ID] = self.id
		
		if self.timer is not None:
			object[TimerTask.MongoDBFields.Timer] = self.timer.to_json()
		return object

	def to_json(self):
		object = {TimerTask.JSONField.CreationDate: self.creation_date, TimerTask.JSONField.Action: self.action, TimerTask.JSONField.Name: self.name}

		if self.accessory_id is not None:
			object[TimerTask.JSONField.AccessoryID] = str(self.accessory_id)

		if self.user_id is not None:
			object[TimerTask.JSONField.UserID] = str(self.user_id)

		if self.id is not None:
			object[TimerTask.JSONField.ID] = str(self.id)
		
		if self.timer is not None:
			object[TimerTask.JSONField.Timer] = self.timer.to_json()

		return object