import json

class AppAPI:
	class Constants:
		AccessoriesTopic = "accessories"
		NotesTopic = "notes"
		TasksTopic = "tasks"
		UsersTopic = "users"
		AccessoriesLogsTopic = "accessories_logs"

	class Error:

		errors = []

		class Message:
			massage = None
			def __init__(self, message):
				self.message = message

			def json_object(self):
				return {"message": self.message}

		def json_object(self):
			return {"errors": self.errors}

		def __init__(self, messages = []):
			for message in messages:
				self.errors.append(AppAPI.Error.Message(message).json_object())

		def __str__(self):
			return json.dumps(self.json_object())
