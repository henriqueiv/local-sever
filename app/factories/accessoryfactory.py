from app.factories.abstractfactory import AbstractFactory
from app.models.accessory import Accessory
import pymongo
from bson.objectid import ObjectId

class AccessoryFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.accessory

	def validate_accessory_with_id(self, accessory_id):
		accessory = self.find_accessory(accessory_id)
		if accessory_id is None:
			raise Exception("accessory id can not be empty")
		elif accessory is None:
			raise Exception("accessory with id `" + str(accessory_id) + "` does not exists")


	def find_accessory(self, accessory_id):
		objc_accessory_id = ObjectId(str(accessory_id))
		if objc_accessory_id is None:
			raise Exception("accessory id `" + str(accessory_id) + "` is not in a correct format")
			return None

		accessories = self.table.find({"_id": objc_accessory_id})
		for accessory in accessories:
			return Accessory.from_mongo_object(accessory)

		return None

	def get_accessories_for_api(self):
		accessories = self.table.find()
		accessories_json = []
		for mongo_accessory in accessories:
			accessory = Accessory.from_mongo_object(mongo_accessory)
			accessories_json.append(accessory.to_json())

		response = {
			"accessories": accessories_json
		}

		return response

	def insert_or_update(self, accessory):
		where = None

		if accessory.id is not None:
			where = {Accessory.MongoDBField.ID: ObjectId(str(accessory.id))}

		accessory_mongo_object = accessory.mongo_json_representation()
		if accessory_mongo_object.has_key(Accessory.MongoDBField.ID):
			accessory_mongo_object.pop(Accessory.MongoDBField.ID)

		if where is not None and self.table.find(where).count() > 0:
			self.table.update(where, accessory_mongo_object,True)
		else:
			self.table.insert(accessory_mongo_object)

		accessory.id = None