from library.Database import Database

db = Database("library/data/wealth.json")

class Checks:
	
	@staticmethod
	def WalletCheck(user_id ,value : int):
		if isinstance(value, int):
			if user_id in db.filedata:
				userdata = db.filedata[user_id]
				return userdata["wallet"] >= value
		else:
			raise TypeError
		
	@staticmethod
	def BankCheck(user_id ,value : int):
		if isinstance(value, int):
			if user_id in db.filedata:
				userdata = db.filedata[user_id]
				return userdata["bank"] >= value
		else:
			raise TypeError
