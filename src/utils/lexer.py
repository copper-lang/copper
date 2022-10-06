from .tokens import Tokens
class Lexer:
	def __init__(self, line, error):
		self.line = list(line)
		self.error = error
		self.tokens = {}
	
		self.builtins = {
			"out": Tokens.Procs.Builtins.Output()
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
			self.line = self.line[1:-1]
	
			commas = []
			spaces = []
			for i, char in enumerate("".join(self.line)):
				if char == ",":
					commas.append(i)
				elif char == " ":
					spaces.append(i)
	
			args = "".join(self.line).split(",")
	
			try:
				for i in range(len(args)):
					if (args[i].strip()[0] == "\"" and args[i].strip()[-1] != "\"") and (args[i+1].strip()[0] != "\"" and args[i+1].strip()[-1] == "\""):
						args[i] += args[i+1]
						args.pop(i+1)
	
					else:
						arg = ""
						index = i
						while True:
							if args[index][-1] == "\"":
								arg += args[index]
								args.pop(index)
								break
	
							else:
								arg += args[index] + ","
								args.pop(index)
	
						args.insert(i, arg.strip())
	
			except IndexError:
				pass
	
			self.tokens["ARGS"] = []
			for arg in args:
				if arg[0] == "\"" and arg[-1] == "\"":
					self.tokens["ARGS"].append(Tokens.Literals.String(arg[1:-1]))
	
				else:
					self.error.print_stacktrace("LiteralError", f"Invalid literal ('{arg}') passed as argument")
	
			return self.tokens
	
		else:
			self.error.print_stacktrace("SyntaxError", "Missing parentheses")