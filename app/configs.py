import os
import json

class MongoConfig:
	server_address = "localhost"
	server_port = 27017
	db_name = "420bits"

class ArduinoAccessoryConfig:
	i2c_address = 0x04

class ServiceConfig:
	loop_wait_seconds = 30

class AccessoryLoggerConfig:
	min_interval_between_logs = 30


tried_load_file = False
if not tried_load_file:
	tried_load_file = True

	file_dir = os.path.dirname(os.path.abspath(__file__))
	file_path = os.path.join(file_dir, "prefs.py")

	if os.path.isfile(file_path):
		from app import prefs