from app.models.timertask import TimerTask, TaskActionTurnOn, TaskActionTurnOff
from app.factories.timertaskfactory import TimerTaskFactory
from app.managers.accessorymanager import AccessoryManager
import requests

class TaskManager:

	accessory_manager = AccessoryManager()
	

	def run_tasks(self):
		timer_task_factory = TimerTaskFactory()
		tasks = timer_task_factory.get_tasks()
		
		print "Tasks to run: " + str(tasks)

		for task in tasks:
			if not task.can_execute() or task.accessory is None or task.accessory.id is None:
				continue

			action = task.action
			accessory = task.accessory

			if action == TaskActionTurnOn:
				self.accessory_manager.turn_on_accessory(accessory.id)
				self.notify_socket_clients()
				print "Did turn on"
			elif action == TaskActionTurnOff:
				self.accessory_manager.turn_off_accessory(accessory.id)
				self.notify_socket_clients()
				print "Did turn off"

	def notify_socket_clients(self):
		try:
			# TODO: Update clients
			print "Clients updated"
		except:
			print "Clients couldn't be updated"
		

