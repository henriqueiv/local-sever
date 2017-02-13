import time
from app.factories import TimerTaskFactory
from app.task_manager import TaskManager
from app.accessory_logger import AccessoryLogger

task_manager = TaskManager()
timer_task_factory = TimerTaskFactory()

while True:
	accessory_logger = AccessoryLogger()

	task_manager.run_tasks(timer_task_factory.get_tasks())
	accessory_logger.log()

	time.sleep(30)