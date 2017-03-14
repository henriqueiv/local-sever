from app.models.mongodbmodel import MongoDBModel
from app.models.accessory import Accessory

class AccessoryLog(MongoDBModel):
	accessory = None
	creation_date = 0

	class MongoDBFields:
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
		return {AccessoryLog.MongoDBFields.CreationDate: self.creation_date, AccessoryLog.MongoDBFields.Accessory: accessory_object}

	def to_json(self):
		accessory_object = self.accessory.to_json() if self.accessory is not None else {}
		return {AccessoryLog.JSONFields.CreationDate: self.creation_date, AccessoryLog.JSONFields.Accessory: accessory_object}		

	@classmethod
	def from_mongo_object(cls, mongo_object):
		creation_date = mongo_object[AccessoryLog.MongoDBFields.CreationDate] if mongo_object.has_key(AccessoryLog.MongoDBFields.CreationDate) else None
		raw_accessory = mongo_object[AccessoryLog.MongoDBFields.Accessory] if mongo_object.has_key(AccessoryLog.MongoDBFields.Accessory) else None
		accessory = None

		if raw_accessory is not None:
			accessory = Accessory.from_mongo_object(raw_accessory)

		obj = cls(accessory, creation_date)

		return obj