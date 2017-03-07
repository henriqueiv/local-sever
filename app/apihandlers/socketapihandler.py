from app.models.socketmessage import SocketMessage, SocketMessageActionRead, SocketMessageActionTurnOn, SocketMessageActionTurnOff
from app.managers.accessorymanager import AccessoryManager

class SocketAPIHandler:

	accessory_manager = AccessoryManager()
	on_update = None
	on_read = None

	def execute_update(self, from_remote = False):
		if self.on_update is not None:
			self.on_update(from_remote)

	def execute_read(self, message, from_remote):
		if self.on_read is not None:
			self.on_read(message, from_remote)

	def dispatch(self, message, from_remote):
		socket_message = SocketMessage(message)
		if socket_message.action is None:
			print "Error: Action property not received in message: " + message
			return

		if socket_message.action == SocketMessageActionTurnOn and socket_message.id is not None:
			self.accessory_manager.turn_on_accessory(socket_message.id)
			self.execute_update(from_remote)
			print "Turn on: " + str(socket_message.id)

		elif socket_message.action == SocketMessageActionTurnOff and socket_message.id is not None:
			self.accessory_manager.turn_off_accessory(socket_message.id)
			self.execute_update(from_remote)
			print "Turn off: " + str(socket_message.id)

		elif socket_message.action == SocketMessageActionRead:
			self.execute_read(self.accessory_manager.get_accessories_json(), from_remote)
		else:
			self.execute_read({"error": "Nothing to do"}, from_remote)
