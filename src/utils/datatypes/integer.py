import math
from utils.errors import Error

class Integer:
	def __init__(self, literal, line, lineno, location):
		self.literal = literal
		self.line = line
		self.lineno = lineno
		self.location = location

	def round(self, round_type):
		if round_type == "default":
			return Integer(round(self.literal), self.line, self.lineno, self.location)

		elif round_type == "floor":
			return Integer(math.floor(self.literal), self.line, self.lineno, self.location)
		
		else:
			rte = Error(
				"RoundTypeError",
				f"Unknown round type '{round_type}'",
				self.line,
				self.lineno,
				self.location
			)
			rte.print_stacktrace()