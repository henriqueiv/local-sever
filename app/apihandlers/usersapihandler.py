from app.factories.userfactory import UserFactory
import json
from app.validators import UserPostRequestHandlerValidator, UserDeleteRequestHandlerValidator
from app.models.user import User
from app.models.appapi import AppAPI

class UsersAPIHandler:

	class Constants:
		IDKey = "_id"
		DeletedKey = "deleted"
		UserKey = "user"

	user_factory = UserFactory()

	def get(self, as_string = True):
		objects = self.user_factory.get_users_for_api()
		if as_string:
			return json.dumps(objects)
		else:
			return objects

	def create(self, request_body, as_string = True):
		response = {}
		try:
			post_handler_validator = UserPostRequestHandlerValidator()
			post_handler_validator.validate(request_body)
			if post_handler_validator.has_errors():
				response = AppAPI.Error(post_handler_validator.error_messages).json_object()
			else:
				user = User(request_body)
				user.id = str(self.user_factory.insert(user))

				response = {Constants.Constants.UserKey: user.to_json()}

		except Exception, e:
			response = AppAPI.Error([str(e)]).json_object()
			
		if as_string:
			return json.dumps(response)
		else:
			return response

	def delete(self, request_body, as_string = True):
		response = {}
		try:
			validator = UserDeleteRequestHandlerValidator()
			validator.validate(request_body)

			if validator.has_errors():
				response = AppAPI.Error(validator.error_messages).json_object()
			else:
				object_id = str(request_body["_id"])
				if self.user_factory.delete(object_id):
					response = {UsersAPIHandler.Constants.DeletedKey: object_id}
				else:
					response = AppAPI.Error(["There is not any object with id = `" + str(object_id) + "`"]).json_object()

			pass
		except Exception, e:
			response = AppAPI.Error([str(e)]).json_object()

		if as_string:
			return json.dumps(response)
		else:
			return response