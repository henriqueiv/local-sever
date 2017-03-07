from app.managers.accessorymanager import AccessoryManager
from tornado import websocket
import json

class SocketClientsUpdater(object):
	clients = []

	def add_client(self, client):
		if client not in self.clients:
			self.clients.append(client)

	def remove_client(self, client):
		if client in self.clients:
			self.clients.remove(client)

	def update_client(self, client, object):
		data = json.dumps(object)
		client.write_message(data)

	def update_all_clients(self):
		accessory_manager = AccessoryManager()
		objects = accessory_manager.get_accessories_json()
		self.update_all_clients_with_message(json.dumps(objects))

	def update_all_clients_with_message(self, message):
		for c in self.clients:
			c.write_message(message)