from .tokens import Tokens
class Lexer:
	def __init__(self, line, error):
		self.line = list(line)
		if line[-1] == "\n":
			self.line.pop()
		
		self.error = error
		self.tokens = {}
	
		self.builtins = {
			"out": Tokens.Procs.Builtins.Output(),
			"in": Tokens.Procs.Builtins.Input(),
			"set": Tokens.Procs.Builtins.Variable()
		}
	
	def lex(self) -> dict:
		proc = ""
		i = 0
		while self.line[i] != "(":
			proc += self.line[i]
			i += 1
	
		for char in proc:
			self.line.remove(char)

		try:
			self.tokens["PROC"] = self.builtins[proc]
		except KeyError:
			self.error.print_stacktrace("ProcError", f"Unknown procedure '{proc}'")
	
		if self.line[0] == "(" and self.line[-1] == ")":
			self.line = self.line[1:-1]
	
			commas = []
			for i, char in enumerate("".join(self.line)):
				if char == ",":
					commas.append(i)
	
			args = "".join(self.line).split(",")
			for i in range(len(args)):
				args[i] = args[i].strip()
	
			try:
				for i in range(len(args)):
					if args[i][0] == "\"" and args[i][-1] == "\"":
						pass
					
					elif (args[i][0] == "\"" and args[i][-1] != "\"") and (args[i+1][0] != "\"" and args[i+1][-1] == "\""):
						args[i] += args[i+1]
						args.pop(i+1)
	
					elif (args[i][0] == "\"" and args[i][-1] != "\"") and args[i+1][-1] == "\"":
						arg = ""
						while True:
							if args[i][-1] == "\"":
								arg += args[i]
								args.pop(i)
								break
	
							else:
								arg += args[i] + ","
								args.pop(i)
	
						args.insert(i, arg)

					else:
						pass
	
			except IndexError:
				pass
	
			self.tokens["ARGS"] = []
			for arg in args:
				if arg[0] == "\"" and arg[-1] == "\"":
					self.tokens["ARGS"].append(Tokens.Literals.String(arg[1:-1]))
				else:
					if proc == "set":
						self.tokens["ARGS"].append(arg)
					else:
						self.error.print_stacktrace("LiteralError", f"Invalid literal ('{arg}') passed as argument")

			return self.tokens
	
		else:
			self.error.print_stacktrace("SyntaxError", "Missing parentheses")