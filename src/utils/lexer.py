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
			"round": Tokens.Procs.Builtins.Round()
		}
		self.returns = {
			"in": Tokens.Procs.Builtins.Input(),
			"round": Tokens.Procs.Builtins.Round()
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
				if arg.strip()[0] == "\"" and arg.strip()[-1] == "\"":
					self.tokens["ARGS"].append(Tokens.Literals.String(arg.strip()[1:-1]))
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
						self.tokens["ARGS"].append(arg)
						isVar = True
					elif proc == "cast":
						self.tokens["ARGS"] = [arg.strip() for arg in args]
					else:
						try:
							integer = int(arg)
							self.tokens["ARGS"].append(Tokens.Literals.Integer(integer))
						except ValueError:
							try:
								decimal = float(arg)
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
												
											except (SyntaxError, NameError):
												if arg[0] == "$" and (arg[1] == "\"" and arg[-1] == "\""):
													self.tokens["ARGS"].append(Tokens.Literals.String(self.addVars(arg[1:-1])))
												else:
													isProc = False
													for returns in self.returns.keys():
														if arg.strip()[:len(returns)] == returns:
															isProc = True
		
													if isProc:
														self.tokens["ARGS"].append(arg.strip())
														self.tokens["LEXER"] = Lexer

														if len(self.tokens["ARGS"]) < len(args):
															isProc = False
															for returns in self.returns.keys():
																if args[args.index(arg)].strip()[:len(returns)] == returns:
																	isProc = True
              
															if isProc:
																_args = []
																i = args.index(arg)
																while args[i][-1] != ")":
																	_args.append(args[i])
																	i += 1
																_args.append(args[i])

																self.tokens["ARGS"].pop() 
																self.tokens["ARGS"].append((",".join(_args)).strip())
              
													else:
														for builtin in self.builtins.keys():
															if arg.strip()[:len(builtin)] == builtin:
																self.error.print_stacktrace("ProcError", f"Procedure '{builtin}' does not return a value")
														
														self.error.print_stacktrace("LiteralError", f"Invalid literal '{arg.strip()}'")

			return self.tokens
	
		else:
			self.error.print_stacktrace("SyntaxError", "Missing parentheses")
	
	def addVars(self, string):
		for variable in self.variables.keys():
			if f"%{variable}%" in string:
				string = string.replace(f"%{variable}%", str(self.variables[variable].literal))
	
		return string[1:]