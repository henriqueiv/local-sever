from app.factories.abstractfactory import AbstractFactory
from bson.objectid import ObjectId
from app.models.user import User

class UserFactory(AbstractFactory):

	accessory_factory = AccessoryFactory()

	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.users

	def insert(self, user):
		user_json = user.mongo_json_representation()
		if user_json.has_key("_id") and self.table.find({"_id": ObjectId(user_json["_id"])}).count() > 0:
			object_id = ObjectId(user_json["_id"])
			user_json.pop("_id")
			self.table.update({"_id": object_id}, user_json, True)

			return str(object_id)
		else:
			if user_json.has_key("_id"):
				user_json.pop("_id")
			return str(self.table.insert(user_json))

	def delete(self, user_id):
		result = self.table.delete_many({"_id": ObjectId(user_id)})
		return result.deleted_count > 0