class Accessory:
	type = AccessoryTypeUndefined
	id = 0
	name = ""
	def __init__(self, name, id, type):
		self.type = type
		self.name = name
		self.id = id