from app.factories.abstractfactory import AbstractFactory
from bson.objectid import ObjectId
from app.models.user import User

class UserFactory(AbstractFactory):

	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.user

	def validate_user_with_id(self, user_id):
		result = None
		try:
			mongo_user_id = ObjectId(str(user_id))
			result = self.table.find({"_id": mongo_user_id})
		except Exception as a:
			raise Exception("user id `" + str(user_id) + "` is invalid")

		if user_id is None:		
			raise Exception("user id can not be empty")
		elif result is None or result.count() == 0:
			raise Exception("user with id `" + str(user_id) + "` does not exists")

	def insert(self, user):
		user_json = user.mongo_json_representation()
		if user_json.has_key("_id") and self.table.find({"_id": ObjectId(user_json["_id"])}).count() > 0:
			object_id = ObjectId(user_json["_id"])
			user_json.pop("_id")

			if user_json.has_key("username"):
				user_json.pop("username")

			self.table.update({"_id": object_id}, user_json, True)

			return str(object_id)
		else:

			if self.table.find({"username": user_json["username"]}).count() > 0:
				raise Exception("Username `" + str(user_json["username"]) + "` is not available")

			if user_json.has_key("_id"):
				user_json.pop("_id")
			return str(self.table.insert(user_json))

	def delete(self, user_id):
		result = self.table.delete_many({"_id": ObjectId(user_id)})
		return result.deleted_count > 0

	def get_users_for_api(self):
		users = []

		result = self.table.find()
		for db_user in result:
			model = User.from_mongo_object(db_user)
			json = model.to_json()
			if json.has_key("password"):
				json.pop("password")
			users.append(json)

		return {
			"users": users
		}