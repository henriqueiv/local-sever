import time
from app.accessory_manager import AccessoryManager
from app.factories import AccessoryFactory, AccessoryLogFactory
from app.models import AccessoryLog

from datetime import datetime, date, time

accessory_manager = AccessoryManager()
accessory_factory = AccessoryFactory()
accessory_log_factory = AccessoryLogFactory()

TaskActionTurnOn = "turn_on"
TaskActionTurnOff = "turn_off"

class Task:
	action = None
	accessory_id = None
	status = None
	created_date = None
	def is_valid():
		return False

class Timer:
	year = None
	month = None
	day = None
	hour = None
	minute = None
	seconds = None

	def is_valid():
		now = datetime.now()
		return (self.year is None or self.year == now.year) and
				(self.month is None or self.month == now.month) and
				(self.day is None or self.day == now.day) and
				(self.hour is None or self.hour = now.hour) and
				(self.minute is None or self.minute == now.minute) and
				(self.seconds is None or self.seconds == now.seconds)


class TimerTask(Task):
	timer = None
	

timer = Timer()
timer.year = 2014

task = TimerTask()
task.timer = timer
task.accessory_id = 1
task.action = TaskActionTurnOn



while True:
	timestamp = time.time()
	accessories = accessory_manager.get_accessories()
	for accessory in accessories:

		accessory_factory.insert_or_update(accessory)
		accessory_log_factory.insert(AccessoryLog(accessory, timestamp))

		print accessory

	time.sleep(30)