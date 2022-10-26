import math
from .tokens import Tokens

class Interpreter:
	def __init__(self, tokens, variables, error):
		self.tokens = tokens
		self.variables = variables
		self.error = error

		self.returns = {
			"in": Tokens.Procs.Builtins.Input(),
			"cast": Tokens.Procs.Builtins.Cast(),
			# "round": Tokens.Procs.Builtins.Round()
		}
		self.types = {
			"String": "string",
			"Integer": "int",
			"Float": "float",
			"Boolean": "bool"
		}

	def interpret(self) -> dict:
		if isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Output):
			if len(self.tokens["ARGS"]) > 1:
				extra = self.tokens["ARGS"][-(len(self.tokens["ARGS"]) - 1):]
				extra = ", ".join('\'' + str(arg.literal) + '\'' for arg in extra)
				self.error.print_stacktrace("ArgError", f"Extra argument(s) {extra}")

			string = self.tokens["ARGS"][0].literal
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

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Cast):
			try:
				if self.tokens["ARGS"][1] == "string":
					return Tokens.Literals.String(str(self.variables[self.tokens["ARGS"][0]].literal))

				elif self.tokens["ARGS"][1] == "int":
					return Tokens.Literals.Integer(int(self.variables[self.tokens["ARGS"][0]].literal))
				
				elif self.tokens["ARGS"][1] == "float":
					return Tokens.Literals.Float(float(self.variables[self.tokens["ARGS"][0]].literal))

				elif self.tokens["ARGS"][1] == "bool":
					return Tokens.Literals.Boolean(str(self.variables[self.tokens["ARGS"][0]].literal) == "True")
				
				else:
					self.error.print_stacktrace("ConversionTypeError", f"Invalid conversion type '{self.tokens['ARGS'][1]}'")

			except ValueError:
				self.error.print_stacktrace("ConversionError", f"Could not convert '{self.variables[self.tokens['ARGS'][0]].literal}' (type '{self.types[self.variables[self.tokens['ARGS'][0]].__class__.__name__]}') to '{self.tokens['ARGS'][1]}'")

		return self.variables