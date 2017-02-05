from models import Accessory, AccessoryLog
import pymongo
from pymongo import MongoClient

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