from utils.objects.objects import Object
from utils.errors import Error

class Interpreter:
	def __init__(self, line, lineno, location):
		self.line = list(line)
		self.lineno = lineno
		self.location = location
		self.og_line = line

	def interpret(self):
		if "".join(self.line)[:3] == "out":
			for char in "out":
				self.line.remove(char)

			if self.line[0] == "(" and self.line[-1] == ")":
				self.line.pop(0)
				self.line.pop()

				object = Object("".join(self.line))
				type = object.checkType()

				if type[0] == "string":
					print(type[1].string)

			else:
				syntaxerror = Error(
					"SyntaxError",
					"Missing parentheses",
					self.og_line,
					self.lineno,
					self.location
				)
				syntaxerror.print_stacktrace()

		elif "".join(self.line)[:2] == "in":
			for char in "in":
				self.line.remove(char)

			if self.line[0] == "(" and self.line[-1] == ")":
				self.line.pop(0)
				self.line.pop()

				object = Object("".join(self.line))
				type = object.checkType()

				if type[0] == "string":
					input(type[1].string)

		else:
			command = ""
			i = 0
			while True:
				if self.line[i] == "(":
					break
				else:
					command += self.line[i]
					i += 1
			
			commanderror = Error(
				"CommandError",
				f"Unknown command '{command}'",
				self.og_line,
				self.lineno,
				self.location
			)
			commanderror.print_stacktrace()