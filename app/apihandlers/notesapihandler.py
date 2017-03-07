import json
from app.factories.notefactory import NoteFactory, NoteFactoryGetParams
from app.validators import NotesPostRequestHandlerValidator, NotesDeleteRequestHandlerValidator
from app.factories.accessoryfactory import AccessoryFactory
from app.validators import NotesPostRequestHandlerValidator, NotesDeleteRequestHandlerValidator
from app.models.note import Note
import time

class NotesAPIHandler:

	note_factory = NoteFactory()
	accessory_factory = AccessoryFactory()

	def delete(self, request_body, as_string = True):
		response = {}
		try:
			validator = NotesDeleteRequestHandlerValidator()
			validator.validate(request_body)

			if validator.has_errors():
				response = {"errors": validator.error_messages}
			else:
				object_id = str(request_body["_id"])
				if self.note_factory.delete(object_id):
					response = {"deleted": object_id}
				else:
					response = {"errors": ["There is not any objetc with id = `" + str(object_id) + "`"]}

		except Exception as e:
			response = {"errors": [{"message": str(e)}]}

		if as_string:
			return json.dumps(response)
		else:
			return response

	def get(self, params = NoteFactoryGetParams(), as_string = True):
		data = self.note_factory.get_notes_for_api(params)
		if as_string:
			return json.dumps(data)
		else:
			return data

	def create(self, json_object = {}, as_string = True):
		response = {}
		try:
			notes_handler_validator = NotesPostRequestHandlerValidator()
			notes_handler_validator.validate(json_object)

			if notes_handler_validator.has_errors():
				response = {"errors": notes_handler_validator.error_messages}
			else:
				note = Note(json_object)
				note.creation_date = time.time()

				note.id = str(self.note_factory.insert(note))
				response = self.note_factory.get_note_for_api(note.id)

		except Exception as e:
			response = {"errors": [{"message": str(e)}]}

		if as_string:
			return json.dumps(response)
		else:
			return response
