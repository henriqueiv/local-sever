from models import Accessory, AccessoryTypeHumidity, AccessoryTypeTemperature, AccessoryTypeCO2
import smbus

DefaultHumidityAccessoryID = 1
DefaultTemperatureAccessoryID = 2
DefaultCO2AccessoryID = 3

def StringToBytes(val):
  retVal = []
  for c in val:
    retVal.append(ord(c))
  return retVal

class ArduinoAccessories:
	i2cbus = smbus.SMBus(1)
	address = 0x04

	def get_accessories(self):
		bytes = self.i2cbus.read_i2c_block_data(self.address, 0)
		data = "".join(map(chr, bytes)).strip("\xff")
		items = data.split("|")

		humidity = items[0]
		temperature = items[1]
		co2 = items[3]

		accessories = [
			Accessory("Humidity",DefaultHumidityAccessoryID, AccessoryTypeHumidity, humidity),
			Accessory("Temperature",DefaultTemperatureAccessoryID, AccessoryTypeTemperature, temperature),
			Accessory("CO2",DefaultCO2AccessoryID, AccessoryTypeCO2, co2)
		]
		return accessories

	def turn_on_accessory(self, accessory_id):
		message = accessory_id + "1"
		self.i2cbus.write_i2c_block_data(self.address, 0, StringToBytes(message))

	def turn_off_accessory(self, accessory_id):
		message = accessory_id + "0"
		self.i2cbus.write_i2c_block_data(self.address, 0, StringToBytes(message))
