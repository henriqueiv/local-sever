import time
from app.task_manager import TaskManager
from app.accessory_logger import AccessoryLogger

task_manager = TaskManager()
accessory_logger = AccessoryLogger()

while True:
	task_manager.run_tasks()
	accessory_logger.log()

	time.sleep(30)