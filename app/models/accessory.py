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

	def to_json(self):
		return self.mongo_json_representation()

	@classmethod
	def from_mongo_object(cls, mongo_object):
		name = mongo_object["name"] if mongo_object.has_key("name") else None
		id = mongo_object["_id"] if mongo_object.has_key("_id") else None
		type = mongo_object["type"] if mongo_object.has_key("type") else None
		value = mongo_object["value"] if mongo_object.has_key("value") else None
		return cls(name,id,type,value)