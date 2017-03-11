import websocket as _websocket
from app.managers.accessorymanager import AccessoryManager
from tornado import websocket
import json

class SocketClientsUpdater(object):
	clients = []
	accessory_manager = AccessoryManager()

	def add_client(self, client):
		if client not in self.clients:
			self.clients.append(client)

	def remove_client(self, client):
		if client in self.clients:
			self.clients.remove(client)

	def update_client(self, client, object):
		if not self.is_client(client):
			return

		data = json.dumps(object)

		print "Client: " + str(client)
		if isinstance(client, _websocket.WebSocketApp):
			client.send(data)
		elif isinstance(client, websocket.WebSocketHandler):
			client.write_message(data)

	def update_all_clients(self, sender):
		objects = self.accessory_manager.get_accessories_json()
		self.update_all_clients_with_object(objects)
		return objects

	def update_all_clients_with_object(self, object):
		for c in self.clients:
			self.update_client(c, object)

	def is_client(self, client):
		return client in self.clients