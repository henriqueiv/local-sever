from models import TimerTask, TaskActionTurnOn, TaskActionTurnOff
from factories import TimerTaskFactory
from accessory_manager import AccessoryManager

class TaskManager:

	accessory_manager = AccessoryManager()

	def run_tasks(self, tasks):
		for task in tasks:
			if not task.can_execute() or task.accessory is None or task.accessory.id is None:
				continue

			action = task.action
			accessory = task.accessory

			if action == TaskActionTurnOn:
				self.accessory_manager.turn_off_accessory(accessory.id)
				print "Did turn on"
			elif action == TaskActionTurnOn:
				self.accessory_manager.turn_on_accessory(accessory.id)
				print "Did turn on"

