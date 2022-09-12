from utils.objects.objects import Object
from utils.errors import Error

class Interpreter:
	def __init__(self, line, variables, lineno, location):
		self.line = list(line)
		if self.line[-1] == "\n":
			self.line.pop()
		
		self.vars = variables
		self.lineno = lineno
		self.location = location
		self.og_line = line

	def interpret(self) -> dict:
		if "".join(self.line)[:3] == "out":
			for char in "out":
				self.line.remove(char)

			if self.line[0] == "(" and self.line[-1] == ")":
				self.line.pop(0)
				self.line.pop()

				object = Object("".join(self.line), self.og_line, self.lineno, self.location)
				type = object.checkType()

				if type[0] == "string":
					newString = self.getVars(type[1].string)

					if newString != None:
						print(newString)
					else:
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

				object = Object("".join(self.line), self.og_line, self.lineno, self.location)
				type = object.checkType()

				if type[0] == "string":
					newString = self.getVars(type[1].string)

					if newString != None:
						input(newString)
					else:
						input(type[1].string)

			else:
				syntaxerror = Error(
					"SyntaxError",
					"Missing parentheses",
					self.og_line,
					self.lineno,
					self.location
				)
				syntaxerror.print_stacktrace()

		elif "".join(self.line[:3]) == "set":
			for char in "set":
				self.line.remove(char)

			if self.line[0] == "(" and self.line[-1] == ")":
				self.line.pop(0)
				self.line.pop()

				split_index = "".join(self.line).find(",")
				var_name = "".join(self.line[:split_index])

				for char in f"{var_name},":
					self.line.remove(char)

				literal = "".join(self.line).strip()

				object = Object(literal, self.og_line, self.lineno, self.location)
				type = object.checkType()

				if type[0] == "string":
					self.vars[var_name] = type[1]

			# print(self.vars)
			return self.vars

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

	def getVars(self, string):
		try:
			og_string = string
	
			first = ""
			i = 0
			while True:
				if string[i] == "%":
					break
				else:
					first += string[i]
					i += 1
	
			string = list(string)
			for char in f"{first}%":
				string.remove(char)
			
			var_name = ""
			i = 0
			while True:
				if string[i] == "%":
					break
				elif string[i] == string[-1]:
					varerror = Error(
						"VarError",
						"Missing '%' in variable call",
						self.og_line,
						self.lineno,
						self.location
					)
					varerror.print_stacktrace()
				else:
					var_name += string[i]
					i += 1
	
			for char in f"{var_name}%":
				string.remove(char)
	
			return first + self.vars[var_name].string + "".join(string)

		except IndexError:
			return None