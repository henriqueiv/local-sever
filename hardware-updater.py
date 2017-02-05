import time
from app.accessory_manager import AccessoryManager

import pymongo
from pymongo import MongoClient

from pprint import pprint

def StringToBytes(val):
  retVal = []
  for c in val:
    retVal.append(ord(c))
  return retVal

def readBus():
  data = ""
  for i in range(0, 1):
          data += chr(bus.read_byte(address));
  print data

client = MongoClient('localhost', 27017)
db = client['420bits']
data_log = db.data_log
accessories = db.accessories


# if accessories.count({"_id": DefaultHumidityAccessoryID}) == 0:
# 	accessories.insert_one({"_id": DefaultHumidityAccessoryID, "name": "Humidity", "type": AccessoryTypeTemperature})

# if accessories.count({"_id": DefaultTemperatureAccessoryID}) == 0:
# 	accessories.insert_one({"_id": DefaultTemperatureAccessoryID, "name": "Temperature"})

# if accessories.count({"_id": DefaultCO2AccessoryID}) == 0:
# 	accessories.insert_one({"_id": DefaultCO2AccessoryID, "name": "CO2"})


accessory_manager = AccessoryManager()

while True:
	
	ts = time.time()
	accessories = accessory_manager.get_accessories()
	for accessory in accessories:
		print accessory

	# data_log.insert_one({"timestamp": ts, "type": AccessoryTypeHumidity, "value": humidity, "accessory": accessories.find_one({"_id": DefaultHumidityAccessoryID})})
	# data_log.insert_one({"timestamp": ts, "type": AccessoryTypeTemperature, "value": temperature, "accessory": accessories.find_one({"_id": DefaultTemperatureAccessoryID})})
	# data_log.insert_one({"timestamp": ts, "type": AccessoryTypeCO2, "value": co2, "accessory": accessories.find_one({"_id": DefaultCO2AccessoryID})})

	# print data
	time.sleep(30)