from app.factories.abstractfactory import AbstractFactory
from app.factories.accessoryfactory import AccessoryFactory
from bson.objectid import ObjectId
from app.models.note import Note

class NoteFactoryGetParams:
	start_timestamp = None
	end_timestamp = None
	accessory_id = None
	sort_order = 1
	order_by = "timestamp"

	def find_filter_object(self):
		filter_object = {}

		if self.end_timestamp is not None and self.end_timestamp > 0:
			filter_object["end_timestamp"] = str(self.end_timestamp)

		if self.start_timestamp is not None:
			filter_object["start_timestamp"] = str(self.start_timestamp)

		if self.accessory_id is not None:
			filter_object["accessory_id"] = str(self.accessory_id)

		return filter_object

class NoteFactory(AbstractFactory):

	accessory_factory = AccessoryFactory()

	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.notes

	def insert(self, note):
		if note.accessory_id is not None:
			if self.accessory_factory.find_accessory(note.accessory_id) is None:
				raise Exception("Accessory with id `" + str(note.accessory_id) + "` not found")

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
			return self.note_for_api_from_mongo_object(note)
		return None

	def note_for_api_from_mongo_object(self, mongo_object):
		note = Note.from_mongo_object(mongo_object)
		json = note.to_json()

		accessory = self.accessory_factory.find_accessory(note.accessory_id)
		if accessory is not None:
			json["accessory"] = accessory.to_json()
			json.pop("accessory_id")

		return json

	def get_notes_for_api(self, params = NoteFactoryGetParams()):
		notes = self.table.find(params.find_filter_object()).sort(params.order_by, params.sort_order)

		notes_json = []
		for note in notes:
			notes_json.append(self.note_for_api_from_mongo_object(note))

		response = {
			"notes": notes_json
		}

		return response