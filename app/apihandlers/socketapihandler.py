from app.models.socketmessage import SocketMessage, SocketMessageActionRead, SocketMessageActionTurnOn, SocketMessageActionTurnOff
from app.managers.accessorymanager import AccessoryManager

from app.factories.notefactory import NoteFactoryGetParams
from app.apihandlers.notesapihandler import NotesAPIHandler

from app.apihandlers.accessoryapihandler import AccessoryAPIHandler

from app.apihandlers.accessorylogapihandler import AccessoryLogAPIHandler
from app.factories.accessorylogfactory import AccessoryLogFactoryGetParams

from app.apihandlers.tasksapihandler import TasksAPIHandler
from app.factories.timertaskfactory import TaskFactoryGetParams

from app.apihandlers.usersapihandler import UsersAPIHandler

class SocketAPIHandler:

	accessory_manager = AccessoryManager()
	on_update = None
	on_read = None

	def execute_update(self, sender = None):
		if self.on_update is not None:
			self.on_update(sender)

	def execute_read(self, message, sender):
		if self.on_read is not None:
			self.on_read(sender, message)


	def dispatch_notes(self, socket_message, sender):
		notes_api_handler = NotesAPIHandler()

		if socket_message.action == "get_notes":
			params = NoteFactoryGetParams()
			params.from_date = socket_message.argument("from_date")
			params.to_date = socket_message.argument("to_date")
			params.accessory_id = socket_message.argument("accessory_id")
			
			response = notes_api_handler.get(params)

			self.execute_read(response, sender)

		elif socket_message.action == "delete_note" and socket_message.id is not None:
			response = notes_api_handler.delete({"_id": socket_message.id})
			self.execute_read(response, sender)

		elif socket_message.action == "post_note" and socket_message.object is not None:
			response = notes_api_handler.create(socket_message.object)
			self.execute_read(response, sender)

	def dispatch_accessories(self, socket_message, sender):
		accessoryapihandler = AccessoryAPIHandler()
		
		if socket_message.action == "get_accessories":
			response = accessoryapihandler.get_as_json_string()
			self.execute_read(response, sender)

	def dispatch_accessory_log(self, socket_message, sender):
		accessory_log_api_handler = AccessoryLogAPIHandler()

		if socket_message.action == "get_accessories_logs":
			params = AccessoryLogFactoryGetParams()
	        params.from_date = socket_message.argument("from_date")
	        params.to_date = socket_message.argument("to_date")
	        params.accessory_id = socket_message.argument("accessory_id")
	        params.limit = int(socket_message.argument("limit")) if socket_message.argument("limit") is not None else 0
	        
	        response = accessory_log_api_handler.get_as_json_string(params)
	        self.execute_read(response, sender)


	def dispatch_tasks(self, socket_message, sender):
		tasks_api_handler = TasksAPIHandler()

		if socket_message.action == "get_tasks":
			params = TaskFactoryGetParams()
			params.accessory_id = socket_message.argument("accessory_id")
			response = tasks_api_handler.get(params)
			self.execute_read(response, sender)

		elif socket_message.action == "delete_task" and socket_message.id is not None:
			response = tasks_api_handler.delete({"_id": socket_message.id})
			self.execute_read(response, sender)

		elif socket_message.action == "post_task" and socket_message.object is not None:
			response = tasks_api_handler.create(socket_message.object)
			self.execute_read(response, sender)


	def dispatch_users(self, socket_message, sender):
		users_api_handler = UsersAPIHandler()

		if socket_message.action == "get_users":
			self.execute_read(users_api_handler.get(), sender)

		elif socket_message.action == "delete_user" and socket_message.id is not None:
			response = users_api_handler.delete({"_id": socket_message.id})
			self.execute_read(response, sender)

		elif socket_message.action == "post_user" and socket_message.object is not None:
			response = users_api_handler.create(socket_message.object)
			self.execute_read(response, sender)			

	def do_dispatch(self, socket_message, sender):
		notes_actions = ["get_notes", "delete_note", "post_note"]
		accessory_actions = ["get_accessories"]
		accessory_log_actions = ["get_accessories_logs"]
		tasks_actions = ["get_tasks", "delete_task", "post_task"]
		users_actions = ["get_users", "post_user", "delete_user"]

		if socket_message.action is None:
			print "Error: Action property not received in message: " + socket_message
			return

		elif socket_message.action in notes_actions:
			self.dispatch_notes(socket_message, sender)

		elif socket_message.action in accessory_actions:
			self.dispatch_accessories(socket_message, sender)

		elif socket_message.action in accessory_log_actions:
			self.dispatch_accessory_log(socket_message, sender)

		elif socket_message.action in tasks_actions:
			self.dispatch_tasks(socket_message, sender)

		elif socket_message.action in users_actions:
			self.dispatch_users(socket_message, sender)

		elif socket_message.action == SocketMessageActionTurnOn and socket_message.id is not None:
			self.accessory_manager.turn_on_accessory(socket_message.id)
			self.execute_update(sender)
			print "Turn on: " + str(socket_message.id)

		elif socket_message.action == SocketMessageActionTurnOff and socket_message.id is not None:
			self.accessory_manager.turn_off_accessory(socket_message.id)
			self.execute_update(sender)
			print "Turn off: " + str(socket_message.id)

		elif socket_message.action == SocketMessageActionRead:
			self.execute_read(self.accessory_manager.get_accessories_json(), sender)

		else:
			self.execute_read("{\"error\": \"Nothing to do\"}", sender)

	def dispatch(self, message, sender):
		socket_message = SocketMessage(message)

		try:
			self.do_dispatch(socket_message, sender)
		except Exception as e:
			self.execute_read(str(e), sender)
		
