from app.models.mongodbmodel import MongoDBModel

class Note(MongoDBModel):

	class JSONField:
		ID = "_id"
		Text = "text"
		UserID = "user_id"
		CreationDate = "creation_date"
		AccessoryID = "accessory_id"
		AccessoryLogID = "accessory_log_id"

	class MongoDBField:
		ID = "_id"
		Text = "text"
		UserID = "user_id"
		CreationDate = "creation_date"
		AccessoryID = "accessory_id"
		AccessoryLogID = "accessory_log_id"

	id = None
	text = ""
	creation_date = 0.0
	user_id = None
	accessory_id = None
	accessory_log_id = None

	def __init__(self, json_object = None):
		if json_object is None or not isinstance(json_object, dict):
			return

		if json_object.has_key(Note.JSONField.ID):
			self.id = json_object[Note.JSONField.ID]

		self.text = json_object[Note.JSONField.Text] if json_object.has_key(Note.JSONField.Text) else None
		self.user_id = json_object[Note.JSONField.UserID] if json_object.has_key(Note.JSONField.UserID) else None
		self.creation_date = json_object[Note.JSONField.CreationDate] if json_object.has_key(Note.JSONField.CreationDate) else None
		self.accessory_id = json_object[Note.JSONField.AccessoryID] if json_object.has_key(Note.JSONField.AccessoryID) else None
		self.accessory_log_id = json_object[Note.JSONField.AccessoryLogID] if json_object.has_key(Note.JSONField.AccessoryLogID) else None

	def mongo_json_representation(self):
		json_representation_object = {Note.MongoDBField.Text: self.text, Note.MongoDBField.CreationDate: self.creation_date}

		if self.id is not None:
			json_representation_object[Note.MongoDBField.ID] = self.id

		if self.accessory_id is not None:
			json_representation_object[Note.MongoDBField.AccessoryID] = self.accessory_id

		if self.accessory_log_id is not None:
			json_representation_object[Note.MongoDBField.AccessoryLogID] = self.accessory_log_id

		if self.user_id is not None:
			json_representation_object[Note.MongoDBField.UserID] = self.user_id

		return json_representation_object

	def to_json(self):
		json_object = self.mongo_json_representation()
		if json_object.has_key(Note.JSONField.ID):
			json_object[Note.JSONField.ID] = str(json_object[Note.JSONField.ID])

		if json_object.has_key(Note.JSONField.AccessoryID):
			json_object[Note.JSONField.AccessoryID] = str(json_object[Note.JSONField.AccessoryID]) if json_object.has_key(Note.JSONField.AccessoryID) else None

		if json_object.has_key(Note.JSONField.AccessoryLogID):
			json_object[Note.JSONField.AccessoryLogID] = str(json_object[Note.JSONField.AccessoryLogID]) if json_object.has_key(Note.JSONField.AccessoryLogID) else None

		if json_object.has_key(Note.JSONField.UserID):			
			json_object[Note.JSONField.UserID] = str(json_object[Note.JSONField.UserID]) if json_object.has_key(Note.JSONField.UserID) else None
		return json_object

	@classmethod
	def from_mongo_object(cls, mongo_object):
		obj = cls()
		if mongo_object.has_key(Note.MongoDBField.ID):
			obj.id = mongo_object[Note.MongoDBField.ID]

		obj.text = mongo_object[Note.MongoDBField.Text] if mongo_object.has_key(Note.MongoDBField.Text) else None
		obj.user_id = mongo_object[Note.MongoDBField.UserID] if mongo_object.has_key(Note.MongoDBField.UserID) else None
		obj.creation_date = mongo_object[Note.MongoDBField.CreationDate] if mongo_object.has_key(Note.MongoDBField.CreationDate) else None
		obj.accessory_id = mongo_object[Note.MongoDBField.AccessoryID] if mongo_object.has_key(Note.MongoDBField.AccessoryID) else None
		obj.accessory_log_id = mongo_object[Note.MongoDBField.AccessoryLogID] if mongo_object.has_key(Note.MongoDBField.AccessoryLogID) else None
		return obj