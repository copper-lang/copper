from utils.objects.string import String
from utils.objects.integer import Integer
from utils.objects.float import Float
from utils.objects.boolean import Boolean
from utils.errors import Error

class Object:
	def __init__(self, object, line, lineno, location):
		self.object = object
		self.line = line
		self.lineno = lineno
		self.location = location

	def checkType(self) -> str:
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

		else:
			try:
				integer = Integer(int("".join(self.object)))
				return "integer", integer
			except ValueError:
				try:
					decimal = Float(float("".join(self.object)))
					return "float", decimal
				except ValueError:
					if "".join(self.object) == "True" or "".join(self.object) == "False":
						boolean = Boolean("".join(self.object) == "True")
						return "boolean", boolean

					else:
						literal = "".join(self.object)
						ile = Error(
							"InvalidLiteralError",
							f"Invalid literal '{literal}'",
							self.line,
							self.lineno,
							self.location
						)
						ile.print_stacktrace()