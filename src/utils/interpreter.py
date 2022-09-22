from utils.objects import Object
from utils.datatypes.string import String
from utils.datatypes.integer import Integer
from utils.datatypes.float import Float
from utils.datatypes.boolean import Boolean
from utils.errors import Error

class Interpreter:
	def __init__(self, line, variables, functions, isFunction, function, lineno, location):
		self.line = list(line)
		if self.line[-1] == "\n":
			self.line.pop()

		self.vars = variables
		self.functions = functions
		self.isFunction = isFunction
		self.function = function
		self.lineno = lineno
		self.location = location
		self.og_line = line

	def interpret(self) -> dict:
		if self.isFunction == False:
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

			else:
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
								cte = Error(
									"ConversionTypeError",
									f"Cannot convert to type {castTo}",
									self.og_line,
									self.lineno,
									self.location
								)
								cte.print_stacktrace()

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

				elif command == "round":
					for char in "round":
						self.line.remove(char)

					if self.line[0] == "(" and self.line[-1] == ")":
						self.line.pop(0)
						self.line.pop()

						split_index = "".join(self.line).find(",")
						var_name = "".join(self.line[:split_index])

						if self.vars.get(var_name):
							for char in f"{var_name},":
								self.line.remove(char)

							round_type = "".join(self.line).strip()

							try:
								self.vars[var_name] = self.vars[var_name].round(round_type)
							except ValueError:
								roundingerror = Error(
									"RoundingError",
									f"Unable to round '{self.vars[var_name].literal}'",
									self.og_line,
									self.lineno,
									self.location
								)
								roundingerror.print_stacktrace()

				elif command == "proc":
					for char in "proc":
						self.line.remove(char)

					if self.line[0] == "(" and self.line[-1] == ")":
						self.line.pop(0)
						self.line.pop()

						try:
							proc = ""
							i = 0
							while True:
								if self.line[i] == "(":
									break
								else:
									proc += self.line[i]
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

						for char in proc:
							self.line.remove(char)

						if self.line[0] == "(" and self.line[-1] == ")":
							self.line.pop(0)
							self.line.pop()

							params = "".join(self.line).split(",")
							for i in range(len(params)):
								params[i] = params[i].strip()

							args = {}
							for param in params:
								args[param] = ""

							self.functions[proc] = [args]
							self.isFunction = True
							self.function = proc

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
						syntaxerror = Error(
							"SyntaxError",
							"Missing parentheses",
							self.og_line,
							self.lineno,
							self.location
						)
						syntaxerror.print_stacktrace()

				elif command in self.functions.keys():
					for char in command:
						self.line.remove(char)

					if self.line[0] == "(" and self.line[-1] == ")":
						self.line.pop(0)
						self.line.pop()

						params = "".join(self.line).split(",")
						for i in range(len(params)):
							params[i] = params[i].strip()

						try:
							for i in range(len(params)):
								object = Object(params[i], self.vars, self.og_line, self.lineno, self.location)
								type = object.checkType()
								dontCheck = ["integer", "float", "boolean", "math", "input", "variable"]

								if type[0] not in dontCheck:
									if params[i][0] == "\"" and params[i][-1] != "\"":
										if params[i+1][0] != "\"" and params[i+1][-1] == "\"":
											params[i] = ''.join([params[i] for i in [i, i+1]])
											params.pop(i+1)
										else:
											raise SyntaxError
									else:
										if params[i][0] == "\"" and params[i][-1] == "\"":
											pass
										else:
											raise SyntaxError

						except IndexError:
							pass
						except SyntaxError:
							syntaxerror = Error(
								"SyntaxError",
								"Missing quotation marks in argument",
								self.og_line,
								self.lineno,
								self.location
							)
							syntaxerror.print_stacktrace()

						for i in range(len(params)):
							object = Object(params[i], self.vars, self.og_line, self.lineno, self.location)
							type = object.checkType()

							args = list(self.functions[command][0].keys())
							self.functions[command][0][args[i]] = type[1]

						for arg in self.functions[command][1]:
							interpreter = Interpreter(
								arg,
								self.functions[command][0],
								self.functions,
								self.isFunction,
								self.function,
								self.lineno,
								self.location
							)
							interpreter.interpret()

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

		else:
			if self.og_line == "endproc":
				self.isFunction = False
			else:
				try:
					self.functions[self.function][1].append(self.og_line)
				except IndexError:
					self.functions[self.function].append([])
					self.functions[self.function][1].append(self.og_line)

		# print(self.og_line == "endproc")
		# print(self.og_line)
		return self.vars, self.functions, self.isFunction, self.function

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