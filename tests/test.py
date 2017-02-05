import models
import smbus

AccessoryTypeUndefined = -1
AccessoryTypeHumidity = 0
AccessoryTypeTemperature = 1
AccessoryTypeCO2 = 2

DefaultHumidityAccessoryID = 1
DefaultTemperatureAccessoryID = 2
DefaultCO2AccessoryID = 3

class AccessoryManager:
	device = ArduinoAccessories()

	def get_accessories(self):
		return sef.device.get_accessories()

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
			Accessory("Humidity",DefaultHumidityAccessoryID, AccessoryTypeHumidity),
			Accessory("Temperature",DefaultTemperatureAccessoryID, AccessoryTypeTemperature),
			Accessory("CO2",DefaultCO2AccessoryID, AccessoryTypeCO2)
		]
		return accessories


manager = AccessoryManager()
manager.name = "william"

print manager.name

accessory = Accessory("Will","0",AccessoryTypeTemperature)
print accessory.name

print manager.get_accessories()