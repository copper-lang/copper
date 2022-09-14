from utils.datatypes.string import String
from utils.datatypes.integer import Integer
from utils.datatypes.float import Float
from utils.datatypes.boolean import Boolean
from utils.errors import Error
import utils.interpreter

class Object:
	def __init__(self, object, variables, line, lineno, location):
		self.object = object
		self.vars = variables
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

		elif self.vars.get("".join(self.object)):
			return "variable", self.vars.get("".join(self.object))

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
						try:
							command = ""
							i = 0
							while True:
								if self.object[i] == "(":
									break
								else:
									command += self.object[i]
									i += 1

						except IndexError:
							try:
								self.object = "".join(self.object)
								if "^" in self.object:
									self.object.replace("^", "**")

								keys = list(self.vars.keys())
								variables = {}
								for i in range(len(self.vars)):
									variables[keys[i]] = self.vars.get(keys[i]).literal

								result = eval(self.object, variables)

								if isinstance(result, int):
									integer = Integer(result)
									return "math", integer
								else:
									decimal = Float(result)
									return "math", decimal
								
							except SyntaxError:
								literal = "".join(self.object)
								ile = Error(
									"InvalidLiteralError",
									f"Invalid literal '{literal}'",
									self.line,
									self.lineno,
									self.location
								)
								ile.print_stacktrace()

						else:
							interpreter = utils.interpreter.Interpreter(
								self.object,
								self.vars,
								self.lineno,
								self.location
							)

							inpt = String(interpreter.interpret())
							return "input", inpt