import time
from app.accessory_manager import AccessoryManager
from app.factories import AccessoryFactory, AccessoryLogFactory
from app.models import AccessoryLog
from webserver import update_all_clients

accessory_manager = AccessoryManager()
accessory_factory = AccessoryFactory()
accessory_log_factory = AccessoryLogFactory()

while True:
	timestamp = time.time()
	accessories = accessory_manager.get_accessories()
	for accessory in accessories:

		accessory_factory.insert_or_update(accessory)
		accessory_log_factory.insert(AccessoryLog(accessory, timestamp))

		print accessory

	update_all_clients({"hello": "world"})

	time.sleep(30)