import json
from app.factories.timertaskfactory import TimerTaskFactory, TaskFactoryGetParams
from app.validators import TasksDeleteRequestHandlerValidator, TasksPostRequestHandlerValidator
from app.models.timertask import TimerTask
import time

class TasksAPIHandler:

	tasks_factory = TimerTaskFactory()

	def get(self, params = TaskFactoryGetParams(), as_string = True):
		response = {}
		try:
			response = self.tasks_factory.get_tasks_for_api(params)
		except Exception as e:
			response = {"errors": [{"message": str(e)}]}
		
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
				response = {"errors": validator.error_messages}
			else:
				object_id = str(request_body["_id"])
				if self.tasks_factory.delete(object_id):
					response = {"deleted": object_id}
				else:
					response = {"errors": ["There is not any objetc with id `" + str(object_id) + "`"]}

		except Exception, e:
			response = {"errors": [{"message": str(e)}]}

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
				response = {"errors": task_handler_validator.error_messages}
			else:
				timer_task = TimerTask(request_body)
				timer_task.creation_date = time.time()
				timer_task.id = str(self.tasks_factory.insert(timer_task))

				response = timer_task.to_json()

		except Exception, e:
			response = {"errors": [{"message": str(e)}]}

		if as_string:
			return json.dumps(response)
		else:
			return response			