from app.managers.accessorymanager import AccessoryManager
from tornado import websocket

class SocketClientsUpdater(object):
	clients = []

	def update_all_clients(self):
		accessory_manager = AccessoryManager()
		objects = accessory_manager.get_accessories_json()
		self.update_all_clients_with_message(json.dumps(objects))

	def update_all_clients_with_message(self, message):
		for c in self.clients:
			c.write_message(message)