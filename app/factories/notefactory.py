from app.factories.abstractfactory import AbstractFactory
from bson.objectid import ObjectId

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
		note_json = note.mongo_json_representation()
		if note_json.has_key("_id") and self.table.find({"_id": ObjectId(note_json["_id"])}).count() > 0:
			object_id = ObjectId(note_json["_id"])
			note_json.pop("_id")
			self.table.update({"_id": object_id}, note_json, True)

			return str(object_id)
		else:
			note_json.pop("_id")
			return str(self.table.insert(note_json))

	def delete(self, note_id):
		result = self.table.delete_many({"_id": ObjectId(note_id)})
		return result.deleted_count > 0


	def get_notes_for_api(self, params = NoteFactoryGetParams()):
		notes = self.table.find(params.find_filter_object()).sort(params.order_by, params.sort_order)

		notes_json = []
		for note in notes:
			note["_id"] = str(note["_id"])
			notes_json.append(task)

		response = {
			"notes": notes_json
		}

		return response