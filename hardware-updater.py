import time
from app.accessory_manager import AccessoryManager

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['420bits']
data_log = db.data_log
accessories_db = db.accessories


accessory_manager = AccessoryManager()

while True:
	
	ts = time.time()
	accessories = accessory_manager.get_accessories()

	for accessory in accessories:
		accessory_dictionary = accessory.to_json()

		accessories_db.update({"_id": accessory.id}, accessory_dictionary,True)
		data_log.insert_one({"timestamp": ts, "accessory": accessory_dictionary})

		print accessory

	# data_log.insert_one({"timestamp": ts, "type": AccessoryTypeHumidity, "value": humidity, "accessory": accessories.find_one({"_id": DefaultHumidityAccessoryID})})
	# data_log.insert_one({"timestamp": ts, "type": AccessoryTypeTemperature, "value": temperature, "accessory": accessories.find_one({"_id": DefaultTemperatureAccessoryID})})
	# data_log.insert_one({"timestamp": ts, "type": AccessoryTypeCO2, "value": co2, "accessory": accessories.find_one({"_id": DefaultCO2AccessoryID})})

	# print data
	time.sleep(30)