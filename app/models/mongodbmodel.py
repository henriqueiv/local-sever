class MongoDBModel:
	def mongo_json_representation(self):
		return {}

	@classmethod
	def from_mongo_object(cls, mongo_object):
		return None

	def to_json(self):
		return {}