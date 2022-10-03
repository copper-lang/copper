from .tokens import Tokens

class Lexer:
	def __init__(self, line):
		self.line = list(line)
		self.tokens = {}

		self.builtins = {
			"out": Tokens.Procs.Builtins.Output
		}

	def lex(self) -> dict:
		proc = ""
		i = 0
		while self.line[i] != "(":
			proc += self.line[i]
			i += 1

		for char in proc:
			self.line.remove(char)

		self.tokens["PROC"] = self.builtins[proc]

		if self.line[0] == "(" and self.line[-1] == ")":
			self.line.pop(0)
			self.line.pop()

			commas = []
			for i, char in enumerate("".join(self.line)):
				if char == ",":
					commas.append(i)

			args = "".join(self.line).split(",")

			try:
				for i in range(len(args)):
					if (args[i][0] == "\"" and args[i][-1] != "\"") and (args[i+1][0] != "\"" and args[i+1][-1] == "\""):
						args[i] += args[i+1]
						args.pop(i+1)

					elif (args[i-1][0] == "\"" and args[i-1][-1] != "\"") and (args[i][0] != "\"" and args[i][-1] != "\"") and (args[i+1][0] != "\"" and args[i+1][-1] == "\""):
						args[i-1] += args[i]
						args[i-1] += args[i+1]
						args.pop(i+1)
						args.pop(i)

			except IndexError:
				pass

			for i in range(len(commas)):
				if i == commas[i]:
					self.line = list("".join(self.line[i:]) + "," + "".join(self.line[:i]))

			print("".join(self.line))