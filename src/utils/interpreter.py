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
			print(self.tokens["ARGS"][0].literal)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Input):
			return input(self.tokens["ARGS"][0].literal)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Variable):
			try:
				isProc = False
				for returns in self.returns.keys():
					if self.tokens["ARGS"][1][:len(returns)] == returns:
						isProc = True

				if isProc:
					Lexer = self.tokens["LEXER"]
					lexer = Lexer(self.tokens["ARGS"][1], self.variables, self.error)
					tokens = lexer.lex()

					interpreter = Interpreter(tokens, self.variables, self.error)
					returned = interpreter.interpret()

					self.variables[self.tokens["ARGS"][0]] = Tokens.Literals.String(returned)
				
				else:
					self.variables[self.tokens["ARGS"][0]] = self.tokens["ARGS"][1]
			
			except IndexError:
				self.error.print_stacktrace("LiteralError", "No literal provided")

		return self.variables