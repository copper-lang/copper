from .tokens import Tokens

class Interpreter:
	def __init__(self, tokens, error):
		self.tokens = tokens
		self.error = error

	def interpret(self):
		if isinstance(self.tokens["PROC"], Tokens.Procs.Builtins.Output):
			print(self.tokens["ARGS"][0].literal)