import os
import json

class Environment:
	dev = True

class MongoConfig:
	server_address = None
	server_port = None
	db_name = None

class ArduinoAccessoryConfig:
	i2c_address = None

class ServiceConfig:
	loop_wait_seconds = None

class AccessoryLoggerConfig:
	min_interval_between_logs = None

class BitsCloudClientConfig:
	server_address = None
	device_identifier = None


tried_load_file = False
if not tried_load_file:
	tried_load_file = True

	file_dir = os.path.dirname(os.path.abspath(__file__))
	file_path = os.path.join(file_dir, "prefs.py")

	if os.path.isfile(file_path):
		from app import prefs