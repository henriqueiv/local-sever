import time
from app.accessory_manager import AccessoryManager
from app.factories import AccessoryFactory, AccessoryLogFactory, TimerTaskFactory
from app.models import AccessoryLog
from app.task_manager import TaskManager
from accessory_logger import AccessoryLogger

task_manager = TaskManager()
timer_task_factory = TimerTaskFactory()
accessory_logger = AccessoryLogger()


while True:
	
	accessory_logger.log()
	task_manager.run_tasks(timer_task_factory.get_tasks())

	time.sleep(30)