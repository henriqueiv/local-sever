from app.factories.abstractfactory import AbstractFactory
from app.factories.accessoryfactory import AccessoryFactory
from app.factories.notefactory import NoteFactory
from bson.objectid import ObjectId

class AccessoryNoteFactory(AbstractFactory):

	note_factory = NoteFactory()
	accessory_factory = AccessoryFactory()

	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.accessory_note

	def link_note_to_accessory(self, note_id, accessory_id):
		accessory = self.accessory_factory.find_accessory(accessory_id)
		if accessory is None:
			raise Exception("Accessory with `" + str(accessory_id) +"` id not found")

		return accessory