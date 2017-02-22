from app.factories.abstractfactory import AbstractFactory
from app.factories.accessoryfactory import AccessoryFactory
from bson.objectid import ObjectId
from app.models.note import Note

class NoteFactoryGetParams:
	start_timestamp = None
	end_timestamp = None
	sort_order = 1
	order_by = "timestamp"

	def find_filter_object(self):
		filter_object = {}

		if self.end_timestamp is not None and self.end_timestamp > 0:
			filter_object["end_timestamp"] = str(self.end_timestamp)

		if self.start_timestamp is not None:
			filter_object["start_timestamp"] = str(self.start_timestamp)

		return filter_object

class NoteFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.notes

	def insert(self, note):
		if note.accessory_id is not None:
			accessory_factory = AccessoryFactory()
			if accessory_factory.find_accessory(note.accessory_id) is None:
				raise Exception("Accessory with id `" + str(accessory_id) + "` not found")

		note_json = note.mongo_json_representation()
		if note_json.has_key("_id") and self.table.find({"_id": ObjectId(note_json["_id"])}).count() > 0:
			object_id = ObjectId(note_json["_id"])
			note_json.pop("_id")
			self.table.update({"_id": object_id}, note_json, True)

			return str(object_id)
		else:
			if note_json.has_key("_id"):
				note_json.pop("_id")
			return str(self.table.insert(note_json))

	def delete(self, note_id):
		result = self.table.delete_many({"_id": ObjectId(note_id)})
		return result.deleted_count > 0

	def get_note_for_api(self, note_id):
		result = self.table.find({"_id": ObjectId(note_id)})
		for note in result:
			return Note.from_mongo_object(note).to_json()
		return None

	def get_notes_for_api(self, params = NoteFactoryGetParams()):
		notes = self.table.find(params.find_filter_object()).sort(params.order_by, params.sort_order)

		notes_json = []
		for note in notes:
			note["_id"] = str(note["_id"])
			notes_json.append(note)

		response = {
			"notes": notes_json
		}

		return response