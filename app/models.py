AccessoryTypeUndefined = -1
AccessoryTypeHumidity = 0
AccessoryTypeTemperature = 1
AccessoryTypeCO2 = 2

class Accessory:
	type = AccessoryTypeUndefined
	id = 0
	name = ""
	def __init__(self, name, id, type):
		self.type = type
		self.name = name
		self.id = id