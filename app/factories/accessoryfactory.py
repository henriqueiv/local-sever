from app.factories.abstractfactory import AbstractFactory
from app.models.accessory import Accessory
import pymongo

class AccessoryFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.accessories

	def insert_or_update(self, accessory):
		where = {"_id": accessory.id}

		accessory_mongo_object = accessory.mongo_json_representation()
		if self.table.find(where).count() > 0:
			accessory_mongo_object.pop("_id")
			self.table.update(where, accessory_mongo_object,True)
		else:
			self.table.insert(accessory_mongo_object)