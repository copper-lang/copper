import sys
from utils.objects import Object
from utils.datatypes.string import String
from utils.datatypes.integer import Integer
from utils.datatypes.float import Float
from utils.datatypes.boolean import Boolean
from utils.errors import Error

class Interpreter:
	def __init__(self, line, variables, functions, isFunction, function, lineno, location, lines=[]):
		self.line = list(line)
		if self.line[-1] == "\n":
			self.line.pop()

		self.vars = variables
		self.functions = functions
		self.isFunction = isFunction
		self.function = function
		self.lineno = lineno
		self.location = location
		self.lines = lines
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

						object = Object("".join(self.line), self.vars, self.functions, self.isFunction, self.function, self.og_line, self.lineno, self.location)
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

						object = Object("".join(self.line), self.vars, self.functions, self.isFunction, self.function, self.og_line, self.lineno, self.location)
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

						try:
							for char in f"{var_name},":
								self.line.remove(char)
						
						except ValueError:
							syntaxerror = Error(
								"SyntaxError",
								"Missing comma between variable name and literal",
								self.og_line,
								self.lineno,
								self.location
							)
							syntaxerror.print_stacktrace()

						literal = "".join(self.line).strip()

						object = Object(literal, self.vars, self.functions, self.isFunction, self.function, self.og_line, self.lineno, self.location)
						type = object.checkType()

						if self.isFunction:
							self.functions[command][0][var_name] = type[1]
						else:
							self.vars[var_name] = type[1]

					else:
						syntaxerror = Error(
							"SyntaxError",
							"Missing parentheses",
							self.og_line,
							self.lineno,
							self.location
						)
						syntaxerror.print_stacktrace()

				elif command == "cast":
					for char in "cast":
						self.line.remove(char)

					if self.line[0] == "(" and self.line[-1] == ")":
						self.line.pop(0)
						self.line.pop()

						split_index = "".join(self.line).find(",")
						var_name = "".join(self.line[:split_index])

						if self.vars.get(var_name):
							try:
								for char in f"{var_name},":
									self.line.remove(char)
							
							except ValueError:
								syntaxerror = Error(
									"SyntaxError",
									"Missing comma between variable name and cast type",
									self.og_line,
									self.lineno,
									self.location
								)
								syntaxerror.print_stacktrace()

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
							try:
								for char in f"{var_name},":
									self.line.remove(char)
							
							except ValueError:
								syntaxerror = Error(
									"SyntaxError",
									"Missing comma between variable name and round type",
									self.og_line,
									self.lineno,
									self.location
								)
								syntaxerror.print_stacktrace()

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
								object = Object(params[i], self.vars, self.functions, self.isFunction, self.function, self.og_line, self.lineno, self.location)
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
							if self.functions[command][0] == {"": ""}:
								pass
							else:
								syntaxerror = Error(
									"SyntaxError",
									"Missing arguments",
									self.og_line,
									self.lineno,
									self.location
								)
								syntaxerror.print_stacktrace()
							
						except SyntaxError:
							syntaxerror = Error(
								"SyntaxError",
								"Missing quotation marks in argument",
								self.og_line,
								self.lineno,
								self.location
							)
							syntaxerror.print_stacktrace()

						if "".join(params) == "" and "".join(list(self.functions[command][0])) == "":
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
							try:
								for i in range(len(params)):
									object = Object(params[i], self.vars, self.functions, self.isFunction, self.function, self.og_line, self.lineno, self.location)
									type = object.checkType()
		
									args = list(self.functions[command][0].keys())
									self.functions[command][0][args[i]] = type[1]
	
							except IndexError:
								for i in range(len(params)):
									params[i] = f"'{params[i]}'"
								unexpected = ", ".join(params[len(params) - (len(params) - len(self.functions[command][0])):])
								paramerror = Error(
									"ParamError",
									f"Unexpected parameter(s) {unexpected}",
									self.og_line,
									self.lineno,
									self.location
								)
								paramerror.print_stacktrace()
	
							args = []
							for arg in self.functions[command][0]:
								args.append(str(self.functions[command][0][arg].literal))
							
							if params == args:
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
								for i in range(len(params)):
									params[i] = f"'{params[i]}'"
								unexpected = ", ".join(params[len(params) - (len(params) - len(self.functions[command][0])):])
								paramerror = Error(
									"ParamError",
									f"Unexpected parameter(s) {unexpected}",
									self.og_line,
									self.lineno,
									self.location
								)
								paramerror.print_stacktrace()

					else:
						syntaxerror = Error(
							"SyntaxError",
							"Missing parentheses",
							self.og_line,
							self.lineno,
							self.location
						)
						syntaxerror.print_stacktrace()

				elif command == "if":
					for char in "if":
						self.line.remove(char)

					if self.line[0] == "(" and self.line[-1] == ")":
						self.line.pop(0)
						self.line.pop()

						split_index = "".join(self.line).find(",")
						check = self.line[:split_index]

						keys = list(self.vars.keys())
						variables = {}
						for i in range(len(self.vars)):
							variables[keys[i]] = self.vars.get(keys[i]).literal

						try:
							bool_exp = eval("".join(check), variables)
						except SyntaxError:
							paramerror = Error(
								"ParamError",
								"Missing comma between expression and procedure",
								self.og_line,
								self.lineno,
								self.location
							)
							paramerror.print_stacktrace()

						proc = self.line[split_index:]
						proc.pop(0)
						proc = "".join(proc).strip()

						if bool_exp:
							interpreter = Interpreter(
								proc,
								self.vars,
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
			if self.lineno == len(self.lines):
				if self.isFunction == True and self.og_line == "endproc":
					pass
				elif self.isFunction == True and self.og_line != "endproc":
					print(f"\n\033[0;31mUnclosedProcedureError: The procedure '{self.function}' was never closed\033[0;0m\n")
					sys.exit()
			
			if self.og_line == "endproc":
				self.isFunction = False
			else:
				try:
					self.functions[self.function][1].append(self.og_line)
				except IndexError:
					self.functions[self.function].append([])
					self.functions[self.function][1].append(self.og_line)

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

					try:
						og_string = og_string.replace(f"%{var_name}%", str(self.vars[var_name].literal))
					except KeyError:
						varerror = Error(
							"VarError",
							f"Unknown variable '{var_name}'",
							self.og_line,
							self.lineno,
							self.location
						)
						varerror.print_stacktrace()

			return og_string

		else:
			return None