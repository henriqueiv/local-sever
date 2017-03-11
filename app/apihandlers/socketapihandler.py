from app.models.socketmessage import SocketMessage
from app.models.appapi import AppAPI
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

	def execute_update(self, sender):
		if self.on_update is not None:
			self.on_update(sender)

	def execute_read(self, message, sender):
		if self.on_read is not None:
			self.on_read(sender, message)


	def dispatch_notes(self, socket_message, sender):
		notes_api_handler = NotesAPIHandler()

		if socket_message.uri.is_get_action():
			params = NoteFactoryGetParams()
			params.from_date = socket_message.argument(NotesAPIHandler.Constants.FromDateParam)
			params.to_date = socket_message.argument(NotesAPIHandler.Constants.ToDateParam)
			params.accessory_id = socket_message.argument(NotesAPIHandler.Constants.AccessoryIDParam)
			
			response = notes_api_handler.get(params)

			self.execute_read(response, sender)

		elif socket_message.uri.is_delete_action() and socket_message.id is not None:
			response = notes_api_handler.delete({NotesAPIHandler.Constants.IDKey: socket_message.id})
			self.execute_read(response, sender)

		elif socket_message.uri.is_post_action() and socket_message.object is not None:
			response = notes_api_handler.create(socket_message.object)
			self.execute_read(response, sender)

	def dispatch_accessories(self, socket_message, sender):
		accessoryapihandler = AccessoryAPIHandler()
		
		if socket_message.uri.is_get_action():
			response = accessoryapihandler.get_as_json_string()
			self.execute_read(response, sender)

		if socket_message.uri.is_post_action() and socket_message.id is not None:
			state = socket_message.argument("state")
			if state == "on":
				self.accessory_manager.turn_on_accessory(socket_message.id)
				self.execute_update(sender)
				
			elif state == "off":
				self.accessory_manager.turn_off_accessory(socket_message.id)
				self.execute_update(sender)


	def dispatch_accessory_log(self, socket_message, sender):
		accessory_log_api_handler = AccessoryLogAPIHandler()

		if socket_message.uri.is_get_action():
			params = AccessoryLogFactoryGetParams()
			params.from_date = socket_message.argument(AccessoryAPIHandler.Constants.FromDateParam)
			params.to_date = socket_message.argument(AccessoryAPIHandler.Constants.ToDateParam)
			params.accessory_id = socket_message.argument(AccessoryAPIHandler.Constants.AccessoryIDParam)
			params.limit = int(socket_message.argument(AccessoryAPIHandler.Constants.LimitParam,0))
			response = accessory_log_api_handler.get_as_json_string(params)
			self.execute_read(response, sender)
		
	def dispatch_tasks(self, socket_message, sender):
		tasks_api_handler = TasksAPIHandler()

		if socket_message.uri.is_get_action():
			params = TaskFactoryGetParams()
			params.accessory_id = socket_message.argument(TasksAPIHandler.Constants.AccessoryIDKey)
			response = tasks_api_handler.get(params)
			self.execute_read(response, sender)

		elif socket_message.uri.is_delete_action() and socket_message.id is not None:
			response = tasks_api_handler.delete({TasksAPIHandler.Constants.IDKey: socket_message.id})
			self.execute_read(response, sender)
			

		elif socket_message.uri.is_post_action() and socket_message.object is not None:
			response = tasks_api_handler.create(socket_message.object)
			self.execute_read(response, sender)


	def dispatch_users(self, socket_message, sender):
		users_api_handler = UsersAPIHandler()

		if socket_message.uri.is_get_action():
			self.execute_read(users_api_handler.get(), sender)

		elif socket_message.uri.is_delete_action() and socket_message.id is not None:
			response = users_api_handler.delete({UsersAPIHandler.Constants.IDKey: socket_message.id})
			self.execute_read(response, sender)

		elif socket_message.uri.is_post_action() and socket_message.object is not None:
			response = users_api_handler.create(socket_message.object)
			self.execute_read(response, sender)



	def dispatch(self, message, sender):
		socket_message = SocketMessage(message)

		topics = {
			AppAPI.Constants.AccessoriesTopic: self.dispatch_accessories,
			AppAPI.Constants.NotesTopic: self.dispatch_notes,
			AppAPI.Constants.TasksTopic: self.dispatch_tasks,
			AppAPI.Constants.UsersTopic: self.dispatch_users,
			AppAPI.Constants.AccessoriesLogsTopic: self.dispatch_accessory_log
		}

		try:
			if socket_message.uri is None:
				error = str(AppAPI.Error(["`uri` key not sent"]))
				return self.execute_read(error, sender)

			topic = socket_message.uri.topic

			if topic is not None and not topics.has_key(topic):
				error = str(AppAPI.Error(["topic `" + topic + "` is not valid"]))
				return self.execute_read(error, sender)

			elif topic is not None:
				function = topics[topic]
				function(socket_message, sender)

			elif socket_message.uri.is_get_action() and not socket_message.uri.has_topic():
				self.execute_read(self.accessory_manager.get_accessories_json(), sender)

			else:
				error = str(AppAPI.Error(["Nothing to do"]))
				self.execute_read(error, sender)


		except Exception as e:
			error = str(AppAPI.Error(["Unknown error: " + str(e)]))
			self.execute_read(error, sender)
		
