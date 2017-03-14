from app.models.mongodbmodel import MongoDBModel
from bson.objectid import ObjectId

AccessoryTypeUndefined = -1
AccessoryTypeHumidity = 0
AccessoryTypeTemperature = 1
AccessoryTypeCO2 = 2
AccessoryTypeRelay = 3

class Accessory(MongoDBModel):

	class MongoDBFields:
		Name = "name"
		ID = "_id"
		Type = "type"
		Value = "value"

	class JSONFields:
		Name = "name"
		ID = "_id"
		Type = "type"
		Value = "value"

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
		object = {Accessory.MongoDBFields.Name: self.name, Accessory.MongoDBFields.Type: self.type, Accessory.MongoDBFields.Value: self.value}
		if self.id is not None:
			object[Accessory.MongoDBFields.ID] = ObjectId(str(self.id))
		return object

	def to_json(self):
		object = {Accessory.JSONFields.Name: self.name, Accessory.JSONFields.Type: self.type, Accessory.JSONFields.Value: self.value}
		if self.id is not None:
			object[Accessory.JSONFields.ID] = str(self.id)
		return object

	@classmethod
	def from_mongo_object(cls, mongo_object):
		name = mongo_object[Accessory.MongoDBFields.Name] if mongo_object.has_key(Accessory.MongoDBFields.Name) else None
		id = mongo_object[Accessory.MongoDBFields.ID] if mongo_object.has_key(Accessory.MongoDBFields.ID) else None
		type = mongo_object[Accessory.MongoDBFields.Type] if mongo_object.has_key(Accessory.MongoDBFields.Type) else None
		value = mongo_object[Accessory.MongoDBFields.Value] if mongo_object.has_key(Accessory.MongoDBFields.Value) else None

		return cls(name,id,type,value)