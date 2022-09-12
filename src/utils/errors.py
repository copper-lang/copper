import sys

class Error:
	def __init__(self, error_name, reason, line, lineno, location):
		self.error_name = error_name
		self.reason = reason
		self.line = line
		self.lineno = lineno
		self.location = location

	def print_stacktrace(self):
		print(f"\n\033[0;31mError - at line {self.lineno} in <{self.location}>")
		print(f"\t{self.line}")
		print(f"{self.error_name}: {self.reason}\033[0;0m\n")

		sys.exit()