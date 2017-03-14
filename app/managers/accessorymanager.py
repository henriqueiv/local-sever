from app.configs import Environment

if Environment.dev:
	from app.hardwareaccessories.arduinoaccessories_debug import ArduinoAccessories
else:
	from app.hardwareaccessories.arduinoaccessories import ArduinoAccessories
	


class AccessoryManager:
	device = ArduinoAccessories()

	def get_accessories_json(self):
		accessories = self.get_accessories()
		accessories_json = []
		for accessory in accessories:
			accessories_json.append(accessory.to_json())
		return accessories_json

	def get_accessories(self):
		return self.device.get_accessories()

	def turn_off_accessory(self, accessory_id):
		self.device.turn_off_accessory(accessory_id)

	def turn_on_accessory(self, accessory_id):
		self.device.turn_on_accessory(accessory_id)