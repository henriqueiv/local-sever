import time
from accessory_manager import AccessoryManager
from models import AccessoryLog
from factories import AccessoryFactory, AccessoryLogFactory

class AccessoryLogger:

	accessory_factory = AccessoryFactory()
	accessory_log_factory = AccessoryLogFactory()
	accessory_manager = AccessoryManager()

	def log(self):
		timestamp = time.time()
		accessories = self.accessory_manager.get_accessories()
		for accessory in accessories:
			self.accessory_factory.insert_or_update(accessory)
			self.accessory_log_factory.insert(AccessoryLog(accessory, timestamp))
			print accessory
		pass