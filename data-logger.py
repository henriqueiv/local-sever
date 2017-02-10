import time
from app.accessory_manager import AccessoryManager
from app.factories import AccessoryFactory, AccessoryLogFactory, TimerTaskFactory
from app.models import AccessoryLog
from app.task_manager import TaskManager

task_manager = TaskManager()
timer_task_factory = TimerTaskFactory()
accessory_logger = AccessoryLogger()

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


while True:
	
	accessory_logger.log()
	task_manager.run_tasks(timer_task_factory.get_tasks())

	time.sleep(30)