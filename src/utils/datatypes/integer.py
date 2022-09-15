from utils.errors import Error

class Integer:
	def __init__(self, literal, line, lineno, location):
		self.literal = literal
		self.line = line
		self.lineno = lineno
		self.location = location