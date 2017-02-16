import time
from app.managers.taskmanager import TaskManager
from app.loggers.accessorylogger import AccessoryLogger
from app.constants import ServiceConfig

task_manager = TaskManager()
accessory_logger = AccessoryLogger()

while True:
	task_manager.run_tasks()
	accessory_logger.log()

	time.sleep(ServiceConfig.loop_wait_seconds)