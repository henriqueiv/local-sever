import smbus
import time

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


bus = smbus.SMBus(1)
address = 0x04

#bus.write_i2c_block_data(address, 0, StringToBytes("Hello World"))

client = MongoClient('localhost', 27017)
db = client['420bits']
data_log = db.data_log
accessories = db.accessories



Types = [
	"humidity",
	"temperature",
	"co2"
]

DefaultHumidityAccessoryID = 0
DefaultTemperatureAccessoryID = 1
DefaultCO2AccessoryID = 2

AccessoryTypeHumidity = 0
AccessoryTypeTemperature = 1
AccessoryTypeCO2 = 2

if accessories.count({"_id": DefaultHumidityAccessoryID}) == 0:
	accessories.insert_one({"_id": DefaultHumidityAccessoryID, "name": "Humidity", "type": AccessoryTypeTemperature})

if accessories.count({"_id": DefaultTemperatureAccessoryID}) == 0:
	accessories.insert_one({"_id": DefaultTemperatureAccessoryID, "name": "Temperature"})

if accessories.count({"_id": DefaultCO2AccessoryID}) == 0:
	accessories.insert_one({"_id": DefaultCO2AccessoryID, "name": "CO2"})


while True:
	bytes = bus.read_i2c_block_data(address, 0)

	data = "".join(map(chr, bytes)).strip("\xff")

	items = data.split("|")

	humidity = items[0]
	temperature = items[1]
	co2 = items[3]
	ts = time.time()

	data_log.insert_one({"timestamp": ts, "type": 0, "value": humidity})
	data_log.insert_one({"timestamp": ts, "type": 1, "value": temperature})
	result = data_log.insert_one({"timestamp": ts, "type": 2, "value":	 co2})

	cursor = data_log.find_one({"_id": result.inserted_id})
	print cursor
	for document in cursor:
		print document.["_id"]
		#pprint(document)

	print data
	time.sleep(30)