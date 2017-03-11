import json
from app.factories.timertaskfactory import TimerTaskFactory, TaskFactoryGetParams
from app.validators import TasksDeleteRequestHandlerValidator, TasksPostRequestHandlerValidator
from app.models.timertask import TimerTask
import time
from app.models.appapi import AppAPI

class TasksAPIHandler:

	class Constants:
		AccessoryIDKey = "accessory_id"
		IDKey = "_id"
		UserIDKey = "user_id"

	tasks_factory = TimerTaskFactory()

	def get(self, params = TaskFactoryGetParams(), as_string = True):
		response = {}
		try:
			response = self.tasks_factory.get_tasks_for_api(params)
		except Exception as e:
			response = AppAPI.Error([str(e)]).json_object()
		
		if as_string:
			return json.dumps(response)
		else:
			return response

	def delete(self, request_body, as_string = True):
		response = {}
		try:
			validator = TasksDeleteRequestHandlerValidator()
			validator.validate(request_body)

			if validator.has_errors():
				response = AppAPI.Error(validator.error_messages).json_object()
			else:
				object_id = str(request_body[TasksAPIHandler.Constants.IDKey])
				if self.tasks_factory.delete(object_id):
					response = {"deleted": object_id}
				else:
					response = AppAPI.Error(["There is not any objetc with id `" + str(object_id) + "`"]).json_object()

		except Exception, e:
			response = AppAPI.Error([str(e)]).json_object()

		if as_string:
			return json.dumps(response)
		else:
			return response			
	
	def create(self,request_body, as_string = True):
		response = {}
		try:
			task_handler_validator = TasksPostRequestHandlerValidator()
			task_handler_validator.validate(request_body)
			if task_handler_validator.has_errors():
				response = AppAPI.Error(task_handler_validator.error_messages).json_object()
			else:
				timer_task = TimerTask(request_body)
				timer_task.creation_date = time.time()
				timer_task.id = str(self.tasks_factory.insert(timer_task))

				response = timer_task.to_json()

		except Exception, e:
			response = AppAPI.Error([str(e)]).json_object()

		if as_string:
			return json.dumps(response)
		else:
			return response			