from app.models.mongodbmodel import MongoDBModel
from bson.objectid import ObjectId

class User(MongoDBModel):
	id = None
	name = None
	username = None
	password = None

	class JSONField:
		ID = "_id"
		Name = "name"
		Username = "username"
		Password = "password"


	class MongoDBField:
		ID = "_id"
		Name = "name"
		Username = "username"
		Password = "password"

	def __init__(self, json_object):
		if json_object is None or not isinstance(json_object, dict):
			return
			
		self.id = ObjectId(str(json_object[User.JSONField.ID])) if json_object.has_key(User.JSONField.ID) else None
		self.name = json_object[User.JSONField.Name] if json_object.has_key(User.JSONField.Name) else None
		self.username = json_object[User.JSONField.Username] if json_object.has_key(User.JSONField.Username) else None
		self.password = json_object[User.JSONField.Password] if json_object.has_key(User.JSONField.Password) else None
		

	def mongo_json_representation(self):
		mongo_representation_object = {User.MongoDBField.Name: self.name, User.MongoDBField.Username: self.username, User.MongoDBField.Password: self.password}

		if self.id is not None:
			mongo_representation_object[User.MongoDBField.ID] = self.id
		return mongo_representation_object

	def to_json(self):
		json_object = {User.JSONField.Name: self.name, User.JSONField.Username: self.username, User.JSONField.Password: self.password}
		if self.id is not None:
			json_object[User.JSONField.ID] = str(self.id)

		return json_object

	@classmethod
	def from_mongo_object(cls, mongo_object):
		return cls(mongo_object)