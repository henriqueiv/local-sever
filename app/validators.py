class Validator:
    error_messages = []
    validate_fields = []
    sub_fields_map = {}
    not_empty_fields = []

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

            elif field in self.not_empty_fields and len(json_object[field]) == 0:
                error_message = "`" + str(field) + "` can not be empty"
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

class NotesPostRequestHandlerValidator(Validator):
    validate_fields = [
        "text",
        "user"
    ]
    not_empty_fields = [
        "text"
    ]

class NotesDeleteRequestHandlerValidator(Validator):
    validate_fields = ["_id"]

class TasksDeleteRequestHandlerValidator(Validator):
    validate_fields = ["_id"]

class TasksPostRequestHandlerValidator(Validator):
    task_validator = TaskValidator()

    def __init__(self):
        timer_validator = TimerValidator()

        accessory_validator = AccessoryValidator()
        accessory_validator.validate_fields = ["_id"]
        self.task_validator.sub_fields_map = {
            "accessory": accessory_validator,
            "timer": timer_validator
        }


    def validate(self, request_object):
        self.error_messages = []
        self.task_validator.validate(request_object)
        self.error_messages.extend(self.task_validator.error_messages)