from models import Accessory, AccessoryTypeHumidity, AccessoryTypeTemperature, AccessoryTypeCO2, AccessoryTypeRelay
import smbus

DefaultHumidityAccessoryID = 1
DefaultTemperatureAccessoryID = 2
DefaultCO2AccessoryID = 3
DefaultRelay1AccessoryID = 4
DefaultRelay2AccessoryID = 5

def StringToBytes(val):
  retVal = []
  for c in val:
    retVal.append(ord(c))
  return retVal

class ArduinoAccessories:
	i2cbus = smbus.SMBus(1)
	address = 0x04

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
				Accessory("Humidity",DefaultHumidityAccessoryID, AccessoryTypeHumidity, humidity),
				Accessory("Temperature",DefaultTemperatureAccessoryID, AccessoryTypeTemperature, temperature),
				Accessory("CO2",DefaultCO2AccessoryID, AccessoryTypeCO2, co2),
				Accessory("Relay 1",DefaultRelay1AccessoryID, AccessoryTypeRelay, relay1),
				Accessory("Relay 2",DefaultRelay2AccessoryID, AccessoryTypeRelay, relay2)
			]
			print "Accessories: " + str(accessories)
			return accessories
		except:
			print(str(e))
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
