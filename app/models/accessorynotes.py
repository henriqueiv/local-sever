from app.models.mongodbmodel import MongoDBModel

class AccessoryNotes(MongoDBModel):
	accessory = None
	notes = []

	def mongo_json_representation(self):
		
		json_representation_object = {}
		if self.accessory is not None {
			json_representation_object = self.accessory.mongo_json_representation()
		}

		json_representation_object["notes"] = []
		for note in self.notes
			json_representation_object["notes"].append(note.mongo_json_representation())

		return json_representation_object