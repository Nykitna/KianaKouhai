import json

class KianaFileIO:
	def __init__(self, filepath):
		self.filepath = filepath
	
	def std_load(self):
		with open(self.filepath, "r") as f:
			return f.read()
		
	def std_save(self, data):
		with open(self.filepath, "w") as f:
			f.write(data)
		
	def std_append(self, data):
		with open(self.filepath, "a") as f:
			f.write(data)
	
	def json_load(self):
		with open(self.filepath, "r") as f:
			return json.load(f)
	
	def json_save(self, data):
		with open(self.filepath, "w") as f:
			json.dump(data, f)
			
	def json_append(self, data):
		with open(self.filepath, "a") as f:
			json.dump(data, f)