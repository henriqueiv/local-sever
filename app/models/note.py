from app.models.mongodbmodel import MongoDBModel

class Note(MongoDBModel):
	id = None
	text = ""
	creation_date = 0.0
	user_id = None
	accessory_id = None
	accessory_log_id = None

	def __init__(self, json_object):
		if json_object.has_key("_id"):
			self.id = json_object["_id"]

		self.text = json_object["text"] if json_object.has_key("text") else None
		self.user_id = json_object["user_id"] if json_object.has_key("user_id") else None
		self.creation_date = json_object["creation_date"] if json_object.has_key("creation_date") else None
		self.accessory_id = json_object["accessory_id"] if json_object.has_key("accessory_id") else None
		self.accessory_log_id = json_object["accessory_log_id"] if json_object.has_key("accessory_log_id") else None

	def mongo_json_representation(self):
		json_representation_object = {"text": self.text, "creation_date": self.creation_date}

		if self.id is not None:
			json_representation_object["_id"] = self.id

		if self.accessory_id is not None:
			json_representation_object["accessory_id"] = self.accessory_id

		if self.accessory_log_id is not None:
			json_representation_object["accessory_log_id"] = self.accessory_log_id

		if self.user_id is not None:
			json_representation_object["user_id"] = self.user_id

		return json_representation_object

	def to_json(self):
		json_object = self.mongo_json_representation()
		if json_object.has_key("_id"):
			json_object["_id"] = str(json_object["_id"])

		if json_object.has_key("accessory_id"):
			json_object["accessory_id"] = str(json_object["accessory_id"]) if json_object.has_key("accessory_id") else None

		if json_object.has_key("accessory_log_id"):
			json_object["accessory_log_id"] = str(json_object["accessory_log_id"]) if json_object.has_key("accessory_log_id") else None

		if json_object.has_key("user_id"):			
			json_object["user_id"] = str(json_object["user_id"]) if json_object.has_key("user_id") else None
		return json_object

	@classmethod
	def from_mongo_object(cls, mongo_object):
		return cls(mongo_object)