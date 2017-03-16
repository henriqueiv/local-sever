import json

class AppAPI:
	class Topic:
		Accessories = "accessories"
		Notes = "notes"
		Tasks = "tasks"
		Users = "users"
		AccessoriesLogs = "accessories_logs"

	class Error:

		class Message:
			massage = None
			def __init__(self, message):
				self.message = message

			def json_object(self):
				return {"message": self.message}

		errors = []

		def json_object(self):
			return {"errors": self.errors}

		def __init__(self, messages = []):
			self.errors = []
			for message in messages:
				self.errors.append(AppAPI.Error.Message(message).json_object())

		def __str__(self):
			return json.dumps(self.json_object())
