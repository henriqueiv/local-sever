import time
from app.accessory_manager import AccessoryManager

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['420bits']
data_log = db.data_log
accessories_db = db.accessories


accessory_manager = AccessoryManager()

class AccessoryFactory:
	client = None
	db = None

	def __init__(self):
		self.client = MongoClient('localhost', 27017)
		self.db = client['420bits']

	def insert_or_update(accessory):
		accessory_dictionary = accessory.to_db_json()

		accessories_db = self.db.accessories
		accessories_db.update({"_id": accessory.id}, accessory_dictionary,True)

accessory_factory = AccessoryFactory()

while True:
	
	ts = time.time()
	accessories = accessory_manager.get_accessories()

	for accessory in accessories:
		accessory_dictionary = accessory.to_db_json()

		accessory_factory.insert_or_update(accessory)
		data_log.insert_one({"timestamp": ts, "accessory": accessory_dictionary})

		print accessory

	time.sleep(30)