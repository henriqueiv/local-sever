import json
from app.classes.socketclientsupdater import SocketClientsUpdater
from tornado import web, websocket
from app.managers.accessorymanager import AccessoryManager

class UpdateClientsHandler(web.RequestHandler):

    accessory_manager = AccessoryManager()    

    clients_updater = None

    def initialize(self, clients_updater):
        self.clients_updater = clients_updater

    @web.asynchronous
    def get(self, *args):        
        accessories = json.dumps(self.accessory_manager.get_accessories_json())

        if self.clients_updater is not None:
        	self.clients_updater.update_all_clients()

        self.write(accessories)
        self.finish()