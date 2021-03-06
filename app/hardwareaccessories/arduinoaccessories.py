from app.models.accessory import Accessory, AccessoryTypeHumidity, AccessoryTypeTemperature, AccessoryTypeCO2, AccessoryTypeRelay
import smbus
from app.configs import ArduinoAccessoryConfig


def StringToBytes(val):
  retVal = []
  for c in val:
    retVal.append(ord(c))
  return retVal

class ArduinoAccessories:
	i2cbus = smbus.SMBus(1)
	address = ArduinoAccessoryConfig.i2c_address

	def get_accessories(self):
		try:
			bytes = self.i2cbus.read_i2c_block_data(self.address, 0)
			data = "".join(map(chr, bytes)).strip("\xff")
			items = data.split("|")

			if len(items) == 0:
				return []

			humidity = items[0]
			temperature = items[1]
			co2 = items[2]
			relay1 = items[3]
			relay2 = items[4]

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
