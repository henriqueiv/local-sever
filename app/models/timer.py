from datetime import datetime

class Timer:
	year = None
	month = None
	day = None
	hour = None
	minute = None
	seconds = None

	def __init__(self, json_object):
		self.year = json_object["year"] if json_object.has_key("year") else None
		self.month = json_object["month"] if json_object.has_key("month") else None
		self.day = json_object["day"] if json_object.has_key("day") else None
		self.hour = json_object["hour"] if json_object.has_key("hour") else None
		self.minute = json_object["minute"] if json_object.has_key("minute") else None
		self.seconds = json_object["seconds"] if json_object.has_key("seconds") else None

	def is_late(self):
		if self.year is None or self.month is None or self.day is None or self.hour is None or self.minute is None or self.seconds is None:
			return False
		try:
			timer_fire_date = datetime(int(str(self.year)), int(str(self.month)), int(str(self.day)), int(str(self.hour)), int(str(self.minute)), int(str(self.seconds)))
			now = datetime.now()
			return now > timer_fire_date
		except:
			return False


	def is_on_time(self):
		now = datetime.now()
		return (self.year is None or self.year == now.year)  and (self.month is None or self.month == now.month) and (self.day is None or self.day == now.day) and (self.hour is None or self.hour == now.hour) and (self.minute is None or self.minute == now.minute) and (self.seconds is None or self.seconds == now.seconds)

	def to_json(self): 
		return {"year": self.year, "month": self.month, "day": self.day, "hour": self.hour, "minute": self.minute, "seconds": self.seconds}