import time
from app.accessory_manager import AccessoryManager
from app.factories import AccessoryFactory, AccessoryLogFactory, TimerTaskFactory
from app.models import AccessoryLog
from app.task_manager import TaskManager


accessory_manager = AccessoryManager()
task_manager = TaskManager()

accessory_factory = AccessoryFactory()
accessory_log_factory = AccessoryLogFactory()
timer_task_factory = TimerTaskFactory()

while True:
	timestamp = time.time()
	accessories = accessory_manager.get_accessories()
	for accessory in accessories:

		accessory_factory.insert_or_update(accessory)
		accessory_log_factory.insert(AccessoryLog(accessory, timestamp))

		print accessory

	tasks = timer_task_factory.get_tasks()
	print "Tasks: " + str(tasks) 
	task_manager.run_tasks(tasks)

	time.sleep(30)