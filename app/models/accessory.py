from app.models.mongodbmodel import MongoDBModel

AccessoryTypeUndefined = -1
AccessoryTypeHumidity = 0
AccessoryTypeTemperature = 1
AccessoryTypeCO2 = 2
AccessoryTypeRelay = 3

class Accessory(MongoDBModel):
	type = AccessoryTypeUndefined
	id = None
	name = ""
	value = None

	def __init__(self, name, id, type, value):
		self.type = type
		self.name = name
		self.id = id
		self.value = value

	def mongo_json_representation(self):
		object = {"name": self.name, "type": self.type, "value": self.value}
		if self.id is not None:
			object["_id"] = int(str(self.id))
		return object