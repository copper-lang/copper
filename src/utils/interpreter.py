from .tokens import Tokens

class Interpreter:
	def __init__(self, tokens, variables, error):
		self.tokens = tokens
		self.variables = variables
		self.error = error

	def interpret(self) -> dict:
		if isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Output):
			print(self.tokens["ARGS"][0].literal)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Input):
			input(self.tokens["ARGS"][0].literal)

		elif isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Variable):
			try:
				self.variables[self.tokens["ARGS"][0]] = self.tokens["ARGS"][1]
			except IndexError:
				self.error.print_stacktrace("LiteralError", "No literal provided")

		return self.variables