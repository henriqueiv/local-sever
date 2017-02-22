from app.factories.abstractfactory import AbstractFactory
from app.models.accessory import Accessory
import pymongo

class AccessoryFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.accessories

	def find_accessory(self, accessory_id):
		accessories = self.table.find({"_id": accessory_id})
		for accessory in accessories:
			return Accessory(accessory["name"], accessory["_id"], accessory["type"], accessory["value"])

		return None

	def get_accessories_for_api(self):
		accessories = self.table.find()
		accessories_json = []
		for accessory in accessories:
			accessory["_id"] = str(accessory["_id"]) 
			accessories_json.append(accessory)

		response = {
			"accessories": accessories
		}

		return response

	def insert_or_update(self, accessory):
		where = {"_id": int(accessory.id)}

		accessory_mongo_object = accessory.mongo_json_representation()
		if self.table.find(where).count() > 0:
			accessory_mongo_object.pop("_id")
			self.table.update(where, accessory_mongo_object,True)
		else:
			self.table.insert(accessory_mongo_object)