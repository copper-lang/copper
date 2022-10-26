from .tokens import Tokens
from .interpreter import Interpreter

class Lexer:
	def __init__(self, line, variables, error):
		self.line = list(line)
		if line[-1] == "\n":
			self.line.pop()

		self.variables = variables
		self.error = error
		self.tokens = {}

		self.builtins = {
			"out": Tokens.Procs.Builtins.Output(),
			"in": Tokens.Procs.Builtins.Input(),
			"set": Tokens.Procs.Builtins.Variable(),
			"cast": Tokens.Procs.Builtins.Cast(),
			# "round": Tokens.Procs.Builtins.Round()
		}
		self.returns = {
			"in": Tokens.Procs.Builtins.Input(),
			"cast": Tokens.Procs.Builtins.Cast(),
			# "round": Tokens.Procs.Builtins.Round()
		}
		self.types = [
			"string",
			"int",
			"float",
			"bool"
		]

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

			try:
				for i in range(len(args)):
					if args[i].strip()[0] == "\"" and args[i].strip()[-1] == "\"":
						pass

					elif ((args[i].strip()[0] == "\"" or args[i].strip()[0] + args[i].strip()[1] == "$\"") and args[i].strip()[-1] != "\"") and args[i+1].strip()[-1] == "\"":
						arg = ""
						while True:
							if args[i].strip()[-1] == "\"":
								arg += args[i]
								args.pop(i)
								break

							else:
								arg += args[i] + ","
								args.pop(i)

						args.insert(i, arg)

			except IndexError:
				pass

			self.tokens["ARGS"] = []
			isVar = False
			for arg in args:
				if arg[-1] == ")" and ((arg.strip()[0] == "\"" and arg.strip()[-2] == "\"") or arg.strip()[:-1] in self.types):
					arg = arg.strip()[:-1]
				
				if arg.strip()[0] == "\"" and arg.strip()[-1] == "\"":
					self.tokens["ARGS"].append(Tokens.Literals.String(arg.strip()[1:-1]))
				elif (arg.strip()[0] == "\"" or arg.strip()[:2] == "$\"") and arg.strip()[-1] == "\"":
					self.tokens["ARGS"].append(Tokens.Literals.String(arg.strip()))
				elif (arg.strip()[0] == "\"" and arg.strip()[-1] != "\"") or (arg.strip()[0] != "\"" and arg.strip()[-1] == "\""):
					for returns in self.returns.keys():
						if arg.strip()[:len(returns)] == returns:
							self.error.print_stacktrace("SyntaxError", f"Missing parentheses in procedure call '{returns}'")
		
					isProc = False
					for returns in self.returns.keys():
						if args[args.index(arg)-1].strip()[:len(returns)] == returns:
							isProc = True

					if isProc == False:
						self.error.print_stacktrace("SyntaxError", f"Missing quotation marks in argument '{arg.strip()}'")
				else:
					if proc == "set" and isVar == False:
						self.tokens["ARGS"].append(arg.strip())
						isVar = True
					else:
						try:
							integer = int(arg.strip())
							self.tokens["ARGS"].append(Tokens.Literals.Integer(integer))
						except ValueError:
							try:
								decimal = float(arg.strip())
								self.tokens["ARGS"].append(Tokens.Literals.Float(decimal))
							except ValueError:
								if arg.strip() == "True" or arg.strip() == "False":
									self.tokens["ARGS"].append(Tokens.Literals.Boolean(arg.strip() == "True"))
								else:
									if arg.strip() in self.variables.keys():
										self.tokens["ARGS"].append(self.variables[arg.strip()])
									else:
										if arg.strip() in self.types:
											self.tokens["ARGS"].append(arg.strip())
										else:
											try:
												if "^" in arg:
													arg = arg.replace("^", "**")
												
												variables = {}
												for variable in self.variables.keys():
													variables[variable] = self.variables[variable].literal
												
												eq = eval(arg.strip(), variables)

												if isinstance(eq, bool):
													self.tokens["ARGS"].append(Tokens.Literals.Boolean(eq))
												elif isinstance(eq, int):
													self.tokens["ARGS"].append(Tokens.Literals.Integer(eq))
												elif isinstance(eq, float):
													self.tokens["ARGS"].append(Tokens.Literals.Float(eq))
												
											except (SyntaxError, NameError, AttributeError):
												isProc = False
												proc = ""
												for returns in self.returns.keys():
													if arg.strip()[:len(returns)] == returns:
														isProc = True
														proc = arg.strip()[:len(returns)]

												if isProc:
													i = args.index(arg)
													_arg = list(arg.strip())
													for char in proc:
														_arg.remove(char)
													args[i] = "".join(_arg)

													self.tokens["LEXER"] = Lexer
			
													if len(args) == 2:
														call = args[1].strip()
														self.tokens["ARGS"].append(proc + call)
			
													else:
														i = 1
														_args = ""
														while args[i][-1] != ")":
															_args += args[i] + ","
															i += 1
														_args += args[i]

														self.tokens["ARGS"].append(proc + _args)
		
												else:
													for builtin in self.builtins.keys():
														if arg.strip()[:len(builtin)] == builtin:
															self.error.print_stacktrace("ProcError", f"Procedure '{builtin}' does not return a value")

													self.error.print_stacktrace("LiteralError", f"Invalid literal '{arg.strip()}'")

		else:
			self.error.print_stacktrace("SyntaxError", "Missing parentheses")
   
		return self.tokens
