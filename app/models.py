AccessoryTypeUndefined = -1
AccessoryTypeHumidity = 0
AccessoryTypeTemperature = 1
AccessoryTypeCO2 = 2

class Accessory:
	type = AccessoryTypeUndefined
	id = 0
	name = ""
	value = None
	def __init__(self, name, id, type, value):
		self.type = type
		self.name = name
		self.id = id
		self.value = value

	def to_db_json(self):
		return {"_id": self.id, "name": self.name, "type": self.type, "value": self.value}

	def to_json(self):
		return {"id": self.id, "name": self.name, "type": self.type, "value": self.value}