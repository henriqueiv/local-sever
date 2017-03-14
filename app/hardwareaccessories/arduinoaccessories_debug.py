from app.models.accessory import Accessory, AccessoryTypeHumidity, AccessoryTypeTemperature, AccessoryTypeCO2, AccessoryTypeRelay
from app.configs import ArduinoAccessoryConfig


def StringToBytes(val):
  retVal = []
  for c in val:
    retVal.append(ord(c))
  return retVal

class ArduinoAccessories:
	def get_accessories(self):
		try:
			
			humidity = "60"
			temperature = "30"
			co2 = "450"
			relay1 = "0"
			relay2 = "1"

			accessories = [
				Accessory("Humidity",None, AccessoryTypeHumidity, humidity),
				Accessory("Temperature",None, AccessoryTypeTemperature, temperature),
				Accessory("CO2",None, AccessoryTypeCO2, co2),
				Accessory("Relay 1",None, AccessoryTypeRelay, relay1),
				Accessory("Relay 2",None, AccessoryTypeRelay, relay2)
			]
			return accessories
		except Exception as e:
			print("Error parsing accesories:" + str(e))
			return []

	def turn_on_accessory(self, accessory_id):
		message = str(int(accessory_id)) + "1"
		try:
			self.i2cbus.write_i2c_block_data(self.address, 0, StringToBytes(message))
		except:
			pass

	def turn_off_accessory(self, accessory_id):
		message = str(int(accessory_id)) + "0"
		try:
			self.i2cbus.write_i2c_block_data(self.address, 0, StringToBytes(message))
		except:
			pass
