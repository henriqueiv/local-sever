import json
from app.classes.socketclientsupdater import SocketClientsUpdater

class UpdateClientsHandler(web.RequestHandler):

    accessory_manager = AccessoryManager()    

    clients_updater = None

    def initialize(self, clients_updater):
        self.clients_updater = clients_updater

    @web.asynchronous
    def get(self, *args):        
        accessories = json.dumps(self.accessory_manager.get_accessories_json())

        update_all_clients_with_message(accessories)

        self.write(accessories)
        self.finish()