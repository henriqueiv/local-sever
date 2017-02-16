from app.models.mongodbmodel import MongoDBModel
from app.models.accessory import Accessory

class AccessoryLog(MongoDBModel):
	accessory = None
	timestamp = 0

	def __init__(self, accessory, timestamp):
		self.accessory = accessory
		self.timestamp = timestamp

	def mongo_json_representation(self):
		accessory_object = self.accessory.mongo_json_representation() if self.accessory is not None else {}
		return {"timestamp": self.timestamp, "accessory": accessory_object}