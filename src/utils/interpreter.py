from .tokens import Tokens

class Interpreter:
	def __init__(self, tokens, variables, error):
		self.tokens = tokens
		self.variables = variables
		self.error = error

		self.returns = {
			"in": Tokens.Procs.Builtins.Input()
		}

	def interpret(self) -> dict:
		if isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Output):
			if len(self.tokens["ARGS"]) > 1:
				extra = self.tokens["ARGS"][-(len(self.tokens["ARGS"]) - 1):]
				extra = ", ".join('\'' + str(arg.literal) + '\'' for arg in extra)
				self.error.print_stacktrace("ArgError", f"Extra arguments {extra}")

			print(self.tokens["ARGS"][0].literal)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Input):
			return input(self.tokens["ARGS"][0].literal)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Variable):
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

		return self.variables