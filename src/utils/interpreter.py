from utils.objects import Object
from utils.datatypes.string import String
from utils.datatypes.integer import Integer
from utils.datatypes.float import Float
from utils.datatypes.boolean import Boolean
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
		try:
			command = ""
			i = 0
			while True:
				if self.line[i] == "(":
					break
				else:
					command += self.line[i]
					i += 1
	
		except IndexError:
			syntaxerror = Error(
				"SyntaxError",
				"Missing parentheses",
				self.og_line,
				self.lineno,
				self.location
			)
			syntaxerror.print_stacktrace()
		
		if command == "out":
			for char in "out":
				self.line.remove(char)
	
			if self.line[0] == "(" and self.line[-1] == ")":
				self.line.pop(0)
				self.line.pop()
	
				object = Object("".join(self.line), self.vars, self.og_line, self.lineno, self.location)
				type = object.checkType()
	
				if type[0] == "variable":
					print(type[1].literal)
				else:
					newString = self.getVars(type[1].literal)
					if newString != None:
						print(newString)
					else:
						print(type[1].literal)
	
			else:
				syntaxerror = Error(
					"SyntaxError",
					"Missing parentheses",
					self.og_line,
					self.lineno,
					self.location
				)
				syntaxerror.print_stacktrace()
	
		elif command == "in":
			for char in "in":
				self.line.remove(char)
	
			if self.line[0] == "(" and self.line[-1] == ")":
				self.line.pop(0)
				self.line.pop()
	
				object = Object("".join(self.line), self.vars, self.og_line, self.lineno, self.location)
				type = object.checkType()
	
				if type[0] == "string":
					newString = self.getVars(type[1].literal)
	
					if newString != None:
						return input(newString)
					else:
						return input(type[1].literal)
	
			else:
				syntaxerror = Error(
					"SyntaxError",
					"Missing parentheses",
					self.og_line,
					self.lineno,
					self.location
				)
				syntaxerror.print_stacktrace()
	
		elif command == "set":
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
	
				object = Object(literal, self.vars, self.og_line, self.lineno, self.location)
				type = object.checkType()
	
				self.vars[var_name] = type[1]
	
		elif command == "cast":
			for char in "cast":
				self.line.remove(char)
	
			if self.line[0] == "(" and self.line[-1] == ")":
				self.line.pop(0)
				self.line.pop()
	
				split_index = "".join(self.line).find(",")
				var_name = "".join(self.line[:split_index])
	
				if self.vars.get(var_name):
					for char in f"{var_name},":
						self.line.remove(char)
	
					castTo = "".join(self.line).strip()
	
					if castTo == "string":
						string = String(str(self.vars[var_name].literal), self.og_line, self.lineno, self.location)
						self.vars[var_name] = string
	
					elif castTo == "integer":
						try:
							integer = Integer(int(self.vars[var_name].literal), self.og_line, self.lineno, self.location)
							self.vars[var_name] = integer
	
						except ValueError:
							conversionerror = Error(
								"ConversionError",
								f"Could not convert '{self.vars[var_name].literal}' to int",
								self.og_line,
								self.lineno,
								self.location
							)
							conversionerror.print_stacktrace()
	
					elif castTo == "float":
						try:
							decimal = Float(float(self.vars[var_name].literal), self.og_line, self.lineno, self.location)
							self.vars[var_name] = decimal
	
						except ValueError:
							conversionerror = Error(
								"ConversionError",
								f"Could not convert '{self.vars[var_name].literal}' to float",
								self.og_line,
								self.lineno,
								self.location
							)
							conversionerror.print_stacktrace()
	
					elif castTo == "boolean":
						if self.vars[var_name].literal == "True" or self.vars[var_name].literal == "False":
							boolean = Boolean(self.vars[var_name].literal == "True", self.og_line, self.lineno, self.location)
							self.vars[var_name] = boolean
	
						else:
							conversionerror = Error(
								"ConversionError",
								f"Could not convert '{self.vars[var_name].literal}' to boolean",
								self.og_line,
								self.lineno,
								self.location
							)
							conversionerror.print_stacktrace()
	
				else:
					uve = Error(
						"UnknownVariableError",
						f"Unknown variable '{var_name}'",
						self.og_line,
						self.lineno,
						self.location
					)
					uve.print_stacktrace()
	
			else:
				syntaxerror = Error(
					"SyntaxError",
					"Missing parentheses",
					self.og_line,
					self.lineno,
					self.location
				)
				syntaxerror.print_stacktrace()
	
		else:
			commanderror = Error(
				"CommandError",
				f"Unknown command '{command}'",
				self.og_line,
				self.lineno,
				self.location
			)
			commanderror.print_stacktrace()
	
		# print(self.vars)
		return self.vars
	
	def getVars(self, string) -> str:
		og_string = string
	
		if "%" in string:
			while True:
				if "%" not in string:
					break
				else:
					first_half = ""
					i = 0
					while True:
						if string[i] == "%":
							break
						else:
							first_half += string[i]
							i += 1
	
					string = list(string)
					for char in first_half + "%":
						string.remove(char)
	
					var_name = ""
					i = 0
					while True:
						if string[i] == "%":
							break
						else:
							var_name += string[i]
							i += 1
	
					for char in var_name + "%":
						string.remove(char)
	
					og_string = og_string.replace(f"%{var_name}%", str(self.vars[var_name].literal))
	
			return og_string
	
		else:
			return None