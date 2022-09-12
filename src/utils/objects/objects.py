from utils.objects.string import String
from utils.errors import Error

class Object:
	def __init__(self, object, line, lineno, location):
		self.object = object
		self.line = line
		self.lineno = lineno
		self.location = location

	def checkType(self):
		if self.object[0] == "\"" and self.object[-1] == "\"":
			self.object = list(self.object)
			self.object.pop(0)
			self.object.pop()

			string = String("".join(self.object))
			return "string", string

		elif (self.object[0] != "\"" and self.object[-1] == "\"") or (self.object[0] == "\"" and self.object[-1] != "\""):
			syntaxerror = Error(
				"SyntaxError",
				"Missing quotation marks",
				self.line,
				self.lineno,
				self.location
			)
			syntaxerror.print_stacktrace()