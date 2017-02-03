import smbus
import time

import pymongo
from pymongo import MongoClient

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
db = client.test_database
data_log = db.data_log

while True:
	bytes = bus.read_i2c_block_data(address, 0)

	data = "".join(map(chr, bytes)).strip("\xff")
	data_log.insert_one({"data": data})


	print data
	time.sleep(1)