import json
from app.factories.notefactory import NoteFactory, NoteFactoryGetParams
from app.validators import NotesPostRequestHandlerValidator, NotesDeleteRequestHandlerValidator
from app.factories.accessoryfactory import AccessoryFactory
from app.validators import NotesPostRequestHandlerValidator, NotesDeleteRequestHandlerValidator
from app.models.note import Note
import time
from app.models.appapi import AppAPI

class NotesAPIHandler:

	class Constants:
		IDKey = "_id"
		FromDateParam = "from_date"
		ToDateParam = "to_date"
		AccessoryIDParam = "accessory_id"
		UserIDKey = "user_id"
		DeletedKey = "deleted"

	note_factory = NoteFactory()
	accessory_factory = AccessoryFactory()

	def delete(self, request_body, as_string = True):
		response = {}
		try:
			validator = NotesDeleteRequestHandlerValidator()
			validator.validate(request_body)

			if validator.has_errors():
				response = AppAPI.Error(validator.error_messages).json_object()
			else:
				object_id = str(request_body[NotesAPIHandler.Constants.IDKey])
				if self.note_factory.delete(object_id):
					response = {NotesAPIHandler.Constants.DeletedKey: object_id}
				else:
					response = AppAPI.Error(["There is not any objetc with id = `" + str(object_id) + "`"]).json_object()

		except Exception as e:
			response = AppAPI.Error([str(e)]).json_object()

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
				response = AppAPI.Error(notes_handler_validator.error_messages).json_object()
			else:
				note = Note(json_object)
				note.creation_date = time.time()

				note.id = str(self.note_factory.insert(note))
				response = self.note_factory.get_note_for_api(note.id)

		except Exception as e:
			response = AppAPI.Error([str(e)]).json_object()

		if as_string:
			return json.dumps(response)
		else:
			return response
