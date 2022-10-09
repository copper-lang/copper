import math
from .tokens import Tokens

class Interpreter:
	def __init__(self, tokens, variables, error):
		self.tokens = tokens
		self.variables = variables
		self.error = error

		self.returns = {
			"in": Tokens.Procs.Builtins.Input(),
			"round": Tokens.Procs.Builtins.Round()
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

			print(self.tokens["ARGS"][0].literal)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Input):
			if len(self.tokens["ARGS"]) > 1:
				extra = self.tokens["ARGS"][-(len(self.tokens["ARGS"]) - 1):]
				extra = ", ".join('\'' + str(arg.literal) + '\'' for arg in extra)
				self.error.print_stacktrace("ArgError", f"Extra argument(s) {extra}")

			return input(self.tokens["ARGS"][0].literal)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Variable):
			if len(self.tokens["ARGS"]) > 2:
				extra = self.tokens["ARGS"][-(len(self.tokens["ARGS"]) - 2):]
				extra = ", ".join('\'' + str(arg.literal) + '\'' for arg in extra)
				self.error.print_stacktrace("ArgError", f"Extra argument(s) {extra}")
			
			try:
				for returns in self.returns.keys():
					if self.tokens["ARGS"][1][:len(returns)] == returns:
						break

				Lexer = self.tokens["LEXER"]
				lexer = Lexer(self.tokens["ARGS"][1], self.variables, self.error)
				tokens = lexer.lex()

				interpreter = Interpreter(tokens, self.variables, self.error)
				returned = interpreter.interpret()

				self.variables[self.tokens["ARGS"][0]] = Tokens.Literals.String(returned)
			
			except IndexError:
				self.error.print_stacktrace("LiteralError", "No literal provided")

			except TypeError:
				self.variables[self.tokens["ARGS"][0]] = self.tokens["ARGS"][1]

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Cast):
			try:
				if self.tokens["ARGS"][1] == "string":
					self.variables[self.tokens["ARGS"][0]] = Tokens.Literals.String(str(self.variables[self.tokens["ARGS"][0]].literal))
	
				elif self.tokens["ARGS"][1] == "int":
					self.variables[self.tokens["ARGS"][0]] = Tokens.Literals.Integer(int(self.variables[self.tokens["ARGS"][0]].literal))
				
				elif self.tokens["ARGS"][1] == "float":
					self.variables[self.tokens["ARGS"][0]] = Tokens.Literals.Float(float(self.variables[self.tokens["ARGS"][0]].literal))
	
				elif self.tokens["ARGS"][1] == "bool":
					self.variables[self.tokens["ARGS"][0]] = Tokens.Literals.Boolean(self.variables[self.tokens["ARGS"][0]].literal == "True" or self.variables[self.tokens["ARGS"][0]].literal == True)
				else:
					self.error.print_stacktrace("ConversionTypeError", f"Invalid conversion type '{self.tokens['ARGS'][1]}'")
			except ValueError:
				self.error.print_stacktrace("ConversionError", f"Could not convert '{self.variables[self.tokens['ARGS'][0]].literal}' (type '{self.types[self.variables[self.tokens['ARGS'][0]].__class__.__name__]}') to '{self.tokens['ARGS'][1]}'")
		
		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Round):
			values = [str(self.variables[variable].literal) for variable in self.variables.keys()]
			var_name = [var_name for var_name in self.variables.keys()][values.index(str(self.tokens["ARGS"][0].literal))]
			
			if self.tokens["ARGS"][1].literal == "floor":
				return math.floor(self.tokens["ARGS"][0].literal)
			elif self.tokens["ARGS"][1].literal == "ceil":
				return math.ceil(self.tokens["ARGS"][0].literal)
			elif self.tokens["ARGS"][1].literal == "nearest":
				return round(self.tokens["ARGS"][0].literal)
			else:
				self.error.print_stacktrace("RoundError", f"Invalid round type '{self.tokens['ARGS'][1].literal}'")
  
		return self.variables