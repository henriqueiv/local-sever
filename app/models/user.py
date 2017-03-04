from app.models.mongodbmodel import MongoDBModel

class User(MongoDBModel):
	id = None
	name = None
	username = None
	password = None


	def __init__(self, json_object):
		if json_object.has_key("_id"):
			self.id = json_object["_id"]

		self.id = json_object["_id"] if json_object.has_key("_id") else None
		self.name = json_object["name"] if json_object.has_key("name") else None
		self.username = json_object["username"] if json_object.has_key("username") else None
		self.password = json_object["password"] if json_object.has_key("password") else None
		

	def mongo_json_representation(self):
		json_representation_object = {"name": self.name, "username": self.username, "password": self.password}

		if self.id is not None:
			json_representation_object["_id"] = self.id
		return json_representation_object

	def to_json(self):
		json_object = self.mongo_json_representation()
		if json_object.has_key("_id"):
			json_object["_id"] = str(json_object["_id"])
		return json_object

	@classmethod
	def from_mongo_object(cls, mongo_object):
		return cls(mongo_object)