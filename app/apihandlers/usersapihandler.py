from app.factories.userfactory import UserFactory
import json
from app.validators import UserPostRequestHandlerValidator, UserDeleteRequestHandlerValidator
from app.models.user import User

class UsersAPIHandler:
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
				response = {"errors": post_handler_validator.error_messages}
			else:
				user = User(request_body)
				user.id = str(self.user_factory.insert(user))

				response = {"user": user.to_json()}

		except Exception, e:
			response = {"errors": [{"message": str(e)}]}
			
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
				response = {"errors": validator.error_messages}
			else:
				object_id = str(request_body["_id"])
				if self.user_factory.delete(object_id):
					response = {"deleted": object_id}
				else:
					response = {"errors": ["There is not any object with id = `" + str(object_id) + "`"]}

			pass
		except Exception, e:
			response = {"errors": [{"message": str(e)}]}

		if as_string:
			return json.dumps(response)
		else:
			return response