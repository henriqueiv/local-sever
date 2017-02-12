import json
from datetime import datetime

AccessoryTypeUndefined = -1
AccessoryTypeHumidity = 0
AccessoryTypeTemperature = 1
AccessoryTypeCO2 = 2
AccessoryTypeRelay = 3

SocketMessageActionRead = "read"
SocketMessageActionTurnOn = "turn_on"
SocketMessageActionTurnOff = "turn_off"

TaskActionTurnOn = "turn_on"
TaskActionTurnOff = "turn_off"

class MongoDBModel:
	def mongo_json_representation(self):
		return {}

class Accessory(MongoDBModel):
	type = AccessoryTypeUndefined
	id = None
	name = ""
	value = None

	def __init__(self, name, id, type, value):
		self.type = type
		self.name = name
		self.id = id
		self.value = value

	def mongo_json_representation(self):
		object = {"name": self.name, "type": self.type, "value": self.value}
		if self.id is not None:
			object["_id"] = str(self.id)
		return object


class AccessoryLog(MongoDBModel):
	accessory = None
	timestamp = 0

	def __init__(self, accessory, timestamp):
		self.accessory = accessory
		self.timestamp = timestamp

	def mongo_json_representation(self):
		accessory_object = self.accessory.mongo_json_representation() if self.accessory is not None else {}
		return {"timestamp": self.timestamp, "accessory": accessory_object}

class TimerTask(MongoDBModel):
	id = None
	timer = None
	action = None
	accessory = None
	status = None
	creation_date = None
	name = None

	def __init__(self, json_object):
		if json_object.has_key("_id"):
			self.id = json_object["_id"]

		self.action = json_object["action"] if json_object.has_key("action") else None
		self.status = json_object["status"] if json_object.has_key("status") else None
		self.name = json_object["name"] if json_object.has_key("name") else None
		self.creation_date = json_object["creation_date"] if json_object.has_key("creation_date") else None

		if json_object.has_key("accessory"):
			accessory = json_object["accessory"]
			id = accessory["_id"] if accessory.has_key("_id") else None
			type = accessory["type"] if accessory.has_key("type") else None
			name = accessory["name"] if accessory.has_key("name") else None
			value = accessory["value"] if accessory.has_key("value") else None

			self.accessory = Accessory(name, id, type, value)

		if json_object.has_key("timer"):
			self.timer = Timer(json_object["timer"])

	def can_execute(self):
		return self.timer.is_on_time() or self.timer.is_late()

	def mongo_json_representation(self):
		accessory = self.accessory.mongo_json_representation() if self.accessory is not None else {}
		object = {"status": self.status, "creation_date": self.creation_date, "action": self.action, "accessory": accessory, "name": self.name}
		if self.id is not None:
			object["_id"] = str(self.id)
		
		if self.timer is not None:
			object["timer"] = self.timer.to_json()
		return object

class SocketMessage:
    action = None
    id = None

    def __init__(self, socket_message):
        try:
            message_object = json.loads(socket_message)

            if message_object.has_key("action"):
                self.action = message_object["action"]

            if message_object.has_key("id"):
                self.id = message_object["id"]

        except:
            print("error parsing message:" + str(socket_message))
            return


class Timer:
	year = None
	month = None
	day = None
	hour = None
	minute = None
	seconds = None

	def __init__(self, json_object):
		self.year = json_object["year"] if json_object.has_key("year") else None
		self.month = json_object["month"] if json_object.has_key("month") else None
		self.day = json_object["day"] if json_object.has_key("day") else None
		self.hour = json_object["hour"] if json_object.has_key("hour") else None
		self.minute = json_object["minute"] if json_object.has_key("minute") else None
		self.seconds = json_object["seconds"] if json_object.has_key("seconds") else None

	def is_late(self):
		if self.year is None or self.month is None or self.day is None or self.hour is None or self.minute is None or self.seconds is None:
			return False

		timer_fire_date = datetime(int(str(self.year), int(str(self.month)), int(str(self.day)), int(str(self.hour)), int(str(self.minute)), int(str(self.seconds)))
		now = datetime.now()

		return now > timer_fire_date


	def is_on_time(self):
		now = datetime.now()
		return (self.year is None or self.year == now.year)  and (self.month is None or self.month == now.month) and (self.day is None or self.day == now.day) and (self.hour is None or self.hour == now.hour) and (self.minute is None or self.minute == now.minute) and (self.seconds is None or self.seconds == now.seconds)

	def to_json(self): 
		return {"year": self.year, "month": self.month, "day": self.day, "hour": self.hour, "minute": self.minute, "seconds": self.seconds}