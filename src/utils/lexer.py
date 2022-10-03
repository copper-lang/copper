from tokens import Tokens

class Lexer:
	def __init__(self, line):
		self.line = list(line)
		self.tokens = {}

	def lex(self) -> dict:
		proc = ""
		i = 0
		while self.line[i] != "(":
			proc += self.line[i]
			i += 1

		for char in proc:
			self.line.remove(char)

		if self.line[0] == "(" and self.line[-1] == ")":
			self.line.pop(0)
			self.line.pop()

			args = "".join(self.line).split(",")

			print(args)