from datetime import datetime

class Timer:

	class JSONField:
		Year = "year"
		Month = "month"
		Day = "day"
		Hour = "hour"
		Minute = "minute"
		Seconds = "seconds"
		Timezone = "timezone"

	year = None
	month = None
	day = None
	hour = None
	minute = None
	seconds = None
	timezone = None

	def __init__(self, json_object):
		self.year = json_object[Timer.JSONField.Year] if json_object.has_key(Timer.JSONField.Year) else None
		self.month = json_object[Timer.JSONField.Month] if json_object.has_key(Timer.JSONField.Month) else None
		self.day = json_object[Timer.JSONField.Day] if json_object.has_key(Timer.JSONField.Day) else None
		self.hour = json_object[Timer.JSONField.Hour] if json_object.has_key(Timer.JSONField.Hour) else None
		self.minute = json_object[Timer.JSONField.Minute] if json_object.has_key(Timer.JSONField.Minute) else None
		self.seconds = json_object[Timer.JSONField.Seconds] if json_object.has_key(Timer.JSONField.Seconds) else None
		self.timezone = json_object[Timer.JSONField.Timezone] if json_object.has_key(Timer.JSONField.Timezone) else None

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
		return {Timer.JSONField.Year: self.year, Timer.JSONField.Month: self.month, Timer.JSONField.Day: self.day, Timer.JSONField.Hour: self.hour, Timer.JSONField.Minute: self.minute, Timer.JSONField.Seconds: self.seconds, Timer.JSONField.Timezone: self.timezone}