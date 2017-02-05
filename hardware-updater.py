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
	table = None

	def __init__(self):
		self.client = MongoClient('localhost', 27017)
		self.db = client['420bits']
		self.table = self.db.accessories

	def insert_or_update(self, accessory):
		accessory_dictionary = accessory.to_db_json()

		self.table.update({"_id": accessory.id}, accessory_dictionary,True)

class AccessoryLog:
	accessory = None
	timestamp = 0

	def __init__(self, accessory, timestamp):
		self.accessory = accessory
		self.timestamp = timestamp

class AccessoryLogFactory:
	client = None
	db = None
	table = None

	def __init__(self):
		self.client = MongoClient('localhost', 27017)
		self.db = client['420bits']
		self.table = self.db.data_log

	def insert(self, accessory_log):
		data_log.insert_one({"timestamp": accessory_log.timestamp, "accessory": accessory_log.accessory.to_db_json()})


accessory_factory = AccessoryFactory()
accessory_log_factory = AccessoryLogFactory()

while True:
	ts = time.time()
	accessories = accessory_manager.get_accessories()
	for accessory in accessories:

		accessory_factory.insert_or_update(accessory)
		accessory_log_factory.insert(AccessoryLog(accessory, ts))

		print accessory

	time.sleep(30)