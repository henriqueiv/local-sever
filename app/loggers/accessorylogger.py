import time
from app.managers.accessorymanager import AccessoryManager
from app.models.accessorylog import AccessoryLog
from app.factories.accessoryfactory import AccessoryFactory
from app.factories.accessorylogfactory import AccessoryLogFactory
from app.constants import AccessoryLoggerConfig

class AccessoryLogger:

	accessory_factory = AccessoryFactory()
	accessory_log_factory = AccessoryLogFactory()
	accessory_manager = AccessoryManager()
	last_log_timestamp = 0

	def log(self):
		timestamp = time.time()
		if (timestamp + AccessoryLoggerConfig.min_interval_between_logs) < self.last_log_timestamp:
			return

		self.last_log_timestamp = timestamp

		accessories = self.accessory_manager.get_accessories()
		print "Accessories: " + str(accessories)
		for accessory in accessories:
			self.accessory_factory.insert_or_update(accessory)
			self.accessory_log_factory.insert(AccessoryLog(accessory, timestamp))
			print accessory
		pass