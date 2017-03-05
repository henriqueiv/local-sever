from app.models.mongodbmodel import MongoDBModel
from app.models.accessory import Accessory

class AccessoryLog(MongoDBModel):
	accessory = None
	creation_date = 0

	def __init__(self, accessory, creation_date):
		self.accessory = accessory
		self.creation_date = creation_date

	def mongo_json_representation(self):
		accessory_object = self.accessory.mongo_json_representation() if self.accessory is not None else {}
		return {"creation_date": self.creation_date, "accessory": accessory_object}