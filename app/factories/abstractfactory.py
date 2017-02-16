from app.constants import MongoConfig
import pymongo
from pymongo import MongoClient

class AbstractFactory(object):
	client = None
	db = None
	table = None

	def __init__(self):
		self.client = MongoClient(MongoConfig.server_address, MongoConfig.server_port)
		self.db = self.client[MongoConfig.db_name]