from app.factories.abstractfactory import AbstractFactory
from app.factories.accessoryfactory import AccessoryFactory
from app.factories.userfactory import UserFactory
from bson.objectid import ObjectId
from app.models.note import Note

from app.factories.accessorylogfactory import AccessoryLogFactory

class NoteFactoryGetParams:
	from_date = None
	to_date = None
	accessory_id = None
	accessory_log_id = None
	sort_order = 1
	order_by = "creation_date"

	def find_filter_object(self):
		filter_object = {}

		if self.accessory_id is not None:
			filter_object["accessory_id"] = str(self.accessory_id)

		if self.accessory_log_id is not None:
			filter_object["accessory_log_id"] = str(self.accessory_log_id)


		if self.from_date is not None or self.to_date is not None:
			filter_object["creation_date"] = {}

		if self.to_date is not None and self.to_date > 0:
			filter_object["creation_date"]["$lte"] = float(self.to_date)

		if self.from_date is not None:
			filter_object["creation_date"]["$gte"] = float(self.from_date)

		return filter_object

class NoteFactory(AbstractFactory):

	accessory_log_factory = AccessoryLogFactory()
	accessory_factory = AccessoryFactory()
	user_factory = UserFactory()

	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.note

	def insert(self, note):
		note.user_id = ObjectId(str(note.user_id))
		self.user_factory.validate_user_with_id(note.user_id)

		if note.accessory_id is not None:
			note.accessory_id = ObjectId(str(note.accessory_id))
			self.accessory_factory.validate_accessory_with_id(note.accessory_id)

		if note.accessory_log_id is not None:
			note.accessory_log_id = ObjectId(str(note.accessory_log_id))
			self.accessory_log_factory.validate_accessory_log_with_id(note.accessory_log_id)
		
		object_id = None
		note_json = note.mongo_json_representation()
		if note_json.has_key("_id"):
			object_id = ObjectId(note_json["_id"])
			note_json.pop("_id")

		if note_json is not None and self.table.find({"_id": object_id}).count() > 0:
			self.table.update({"_id": object_id}, note_json, True)
			return str(object_id)
		else:
			return str(self.table.insert(note_json))

	def delete(self, note_id):
		result = self.table.delete_many({"_id": ObjectId(note_id)})
		return result.deleted_count > 0

	def get_note_for_api(self, note_id):
		result = self.table.find({"_id": ObjectId(str(note_id))})
		for note in result:
			return self.note_for_api_from_mongo_object(note)

		return None

	def note_for_api_from_mongo_object(self, mongo_object):
		note = Note.from_mongo_object(mongo_object)
		json = note.to_json()
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