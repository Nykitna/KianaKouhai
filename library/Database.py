import json

class Database:
	def __init__(self, filename) -> None:
		self.filename : str = filename
		self.filedata : dict = None
		self.load()
	
	def load(self):
		with open(self.filename, "r") as f:
			self.filedata = json.load(f)
	
	def lookup(self, key : str):
		if key in self.filedata is True:
			return True
		else:
			return False
		
	def add(self, user_id):
		if isinstance(user_id, int) is True:
			str(user_id)
			self.filedata[user_id] = {"wallet": 2000, "bank": 0}
			self.save()
		else:
			self.filedata[user_id] = {"wallet": 2000, "bank": 0}
			self.save()

	def save(self):
		with open(self.filename, "w") as f:
			json.dump(self.filedata, f, indent = 4)