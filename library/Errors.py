class UserNotFound(Exception):
	def __init__(self):
		super().__init__(message = "User not found in database.")

class DuplicateFound(Exception):
	def __init__(self):
		super().__init__(message = "Matching user ID found! Does user already exist?")

class CommandCanceled(Exception):
	def __init__(self):
		super().__init__(message = "Command was canceled.")