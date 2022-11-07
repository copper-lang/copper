from .tokens import Tokens

class Interpreter:
	def __init__(self, tokens, variables, error):
		self.tokens = tokens
		self.variables = variables
		self.error = error

		self.returns = {
			"in": Tokens.Procs.Builtins.Input(),
			"cast": Tokens.Procs.Builtins.Cast()
		}
		self.types = {
			"String": "string",
			"Integer": "int",
			"Float": "float",
			"Boolean": "bool"
		}
		self.arguments = {
			"out": "'output'",
			"in": "'prompt'",
			"set": ["'variable name'", "'literal'"],
			"cast": ["'variable name'", "'type'"],
		}

	def interpret(self) -> dict:
		if isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Output):
			if len(self.tokens["ARGS"]) > 1:
				extra = self.tokens["ARGS"][-(len(self.tokens["ARGS"]) - 1):]
				extra = ", ".join('\'' + str(arg.literal) + '\'' for arg in extra)
				self.error.print_stacktrace("ArgError", f"Extra argument(s) {extra}")

			string = str(self.tokens["ARGS"][0].literal)
			if (string[0] == "\"" or string[:2] == "$\"") and string[-1] == "\"":
				for variable in self.variables.keys():
					if f"%{variable}%" in string:
						string = string.replace(f"%{variable}%", str(self.variables[variable].literal))

				string = string[2:-1]

			print(string)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Input):
			if len(self.tokens["ARGS"]) > 1:
				extra = self.tokens["ARGS"][-(len(self.tokens["ARGS"]) - 1):]
				extra = ", ".join('\'' + str(arg.literal) + '\'' for arg in extra)
				self.error.print_stacktrace("ArgError", f"Extra argument(s) {extra}")

			return Tokens.Literals.String(input(self.tokens["ARGS"][0].literal))

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Variable):
			if len(self.tokens["ARGS"]) > 2 and self.tokens["ARGS"][2] in self.types.values():
				self.tokens["ARGS"].pop()

			if len(self.tokens["ARGS"]) > 2:
				extra = self.tokens["ARGS"][-(len(self.tokens["ARGS"]) - 2):]
				print(self.tokens["ARGS"])
				extra = ", ".join('\'' + str(arg.literal) + '\'' for arg in extra)
				self.error.print_stacktrace("ArgError", f"Extra argument(s) {extra}")

			try:
				for returns in self.returns.keys():
					if self.tokens["ARGS"][1][:len(returns)] == returns:
						break

				lexer = self.tokens["LEXER"](self.tokens["ARGS"][1], self.variables, self.error)
				tokens = lexer.lex()
    
				interpreter = Interpreter(tokens, self.variables, self.error)
				returned = interpreter.interpret()

				self.variables[self.tokens["ARGS"][0]] = returned

			except TypeError:
				self.variables[self.tokens["ARGS"][0]] = self.tokens["ARGS"][1]
			except IndexError:
				self.error.print_stacktrace("ArgError", f"Missing required argument(s) {', '.join(self.arguments['set'][-(len(self.arguments['set']) - len(self.tokens['ARGS'])):])}")

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Cast):
			if len(self.tokens["ARGS"]) > 2:
				extra = self.tokens["ARGS"][-(len(self.tokens["ARGS"]) - 2):]
				extra = ", ".join('\'' + str(arg.literal) + '\'' for arg in extra)
				self.error.print_stacktrace("ArgError", f"Extra argument(s) {extra}")
      
			var_name = list(self.variables.keys())[list(self.variables.values()).index(self.tokens["ARGS"][0])]
      
			try:
				if self.tokens["ARGS"][1] == "string":
					return Tokens.Literals.String(str(self.variables[var_name].literal))

				elif self.tokens["ARGS"][1] == "int":
					return Tokens.Literals.Integer(int(self.variables[var_name].literal))
				
				elif self.tokens["ARGS"][1] == "float":
					return Tokens.Literals.Float(float(self.variables[var_name].literal))

				elif self.tokens["ARGS"][1] == "bool":
					return Tokens.Literals.Boolean(str(self.variables[var_name].literal) == "True")
				
				else:
					self.error.print_stacktrace("ConversionTypeError", f"Invalid conversion type '{self.tokens['ARGS'][1]}'")

			except ValueError:
				self.error.print_stacktrace("ConversionError", f"Could not convert '{self.variables[var_name].literal}' (type '{self.types[self.variables[var_name].__class__.__name__]}') to '{self.tokens['ARGS'][1]}'")
			except IndexError:
				self.error.print_stacktrace("ArgError", f"Missing required argument(s) {', '.join(self.arguments['cast'][-(len(self.arguments['cast']) - len(self.tokens['ARGS'])):])}")

		return self.variables
