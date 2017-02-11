class Validator:
    error_messages = []
    validate_fields = []
    sub_fields_map = {}

    def has_errors(self):
        return len(self.error_messages) > 0

    def validate(self, json_object, in_key = ""):
        self.error_messages = []
        for field in self.validate_fields:
            if not json_object.has_key(field):
                error_message = "`" + str(field) + "` field not sent"
                if len(in_key) > 0:
                    error_message = error_message + " in the `" + in_key + "` field"
                self.error_messages.append(error_message)

            elif self.sub_fields_map.has_key(field):
                sub_validator = self.sub_fields_map[field]
                sub_validator.validate(json_object[field], field)
                self.error_messages.extend(sub_validator.error_messages)

class TimerValidator(Validator):
    validate_fields = [
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "seconds"
    ]

class AccessoryValidator(Validator):
    validate_fields = [
        "type",
        "_id",
        "name",
        "value",
    ]

class TaskValidator(Validator):
    validate_fields = [
        "action",
        "accessory",
        "timer",
    ]

class TasksPostRequestHandlerValidator(Validator):
    task_validator = TaskValidator()
    def validate(self, request_object):
        self.error_messages = []
        self.task_validator.validate(request_object)
        self.error_messages.extend(self.task_validator.error_messages)