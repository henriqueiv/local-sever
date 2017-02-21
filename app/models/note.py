from app.models.mongodbmodel import MongoDBModel

class Note(MongoDBModel):
	id = None
	text = ""
	timestamp = 0.0
	user = 0

	def mongo_json_representation(self):
		json_representation_object = {"text": self.text, "timestamp": self.timestamp, "user": self.user}
		if self.id is not None:
			json_representation_object["_id"] = self.id

		return json_representation_object