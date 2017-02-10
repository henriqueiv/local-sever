from models import TimerTask, TaskActionTurnOn, TaskActionTurnOff
from factories import TimerTaskFactory
from accessory_manager import AccessoryManager
import requests

class TaskManager:

	accessory_manager = AccessoryManager()

	def run_tasks(self, tasks):
		print tasks

		for task in tasks:
			if not task.can_execute() or task.accessory is None or task.accessory.id is None:
				print "task can not run"
				print "Can execute: " + str(task.can_execute())
				print "Aceesory: "+ str(task.accessory)
				print "Timer": + str(task.timer.to_json())
				print task.mongo_json_representation()

				continue

			action = task.action
			accessory = task.accessory

			if action == TaskActionTurnOn:
				self.accessory_manager.turn_off_accessory(accessory.id)
				self.notify_socket_clients()
				print "Did turn on"
			elif action == TaskActionTurnOn:
				self.accessory_manager.turn_on_accessory(accessory.id)
				self.notify_socket_clients()
				print "Did turn on"

	def notify_socket_clients(self):
		try:
			requests.get("http://192.168.0.15:8888/update_clients")
			print "Clients updated"
		except:
			print "Clients couldn't be updated"
		

