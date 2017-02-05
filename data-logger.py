import time
from app.accessory_manager import AccessoryManager
from app.factories import AccessoryFactory, AccessoryLogFactory
from app.models import AccessoryLog

accessory_manager = AccessoryManager()
accessory_factory = AccessoryFactory()
accessory_log_factory = AccessoryLogFactory()

while True:
	ts = time.time()
	accessories = accessory_manager.get_accessories()
	for accessory in accessories:

		accessory_factory.insert_or_update(accessory)
		accessory_log_factory.insert(AccessoryLog(accessory, ts))

		print accessory

	time.sleep(30)