from app.models.mongodbmodel import MongoDBModel
from app.models.accessory import Accessory

class AccessoryLog(MongoDBModel):

	accessory = None
	creation_date = 0

	class MongoDBField:
		CreationDate = "creation_date"
		Accessory = "accessory"

	class JSONFields:
		CreationDate = "creation_date"
		Accessory = "accessory"

	def __init__(self, accessory, creation_date):
		self.accessory = accessory
		self.creation_date = creation_date

	def mongo_json_representation(self):
		accessory_object = self.accessory.mongo_json_representation() if self.accessory is not None else {}
		return {AccessoryLog.MongoDBField.CreationDate: self.creation_date, AccessoryLog.MongoDBField.Accessory: accessory_object}

	def to_json(self):
		accessory_object = self.accessory.to_json() if self.accessory is not None else {}
		return {AccessoryLog.JSONFields.CreationDate: self.creation_date, AccessoryLog.JSONFields.Accessory: accessory_object}		

	@classmethod
	def from_mongo_object(cls, mongo_object):
		creation_date = mongo_object[AccessoryLog.MongoDBField.CreationDate] if mongo_object.has_key(AccessoryLog.MongoDBField.CreationDate) else None
		raw_accessory = mongo_object[AccessoryLog.MongoDBField.Accessory] if mongo_object.has_key(AccessoryLog.MongoDBField.Accessory) else None
		accessory = None

		if raw_accessory is not None:
			accessory = Accessory.from_mongo_object(raw_accessory)

		obj = cls(accessory, creation_date)

		return obj