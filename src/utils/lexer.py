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
            "set": Tokens.Procs.Builtins.Variable()
        }
        self.returns = {
            "in": Tokens.Procs.Builtins.Input()
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

                    else:
                        pass

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
                    
                    self.error.print_stacktrace("SyntaxError", f"Missing quotation marks in argument '{arg.strip()}'")
                else:
                    if proc == "set" and isVar == False:
                        self.tokens["ARGS"].append(arg)
                        isVar = True
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
                                        try:
                                            if "^" in arg.strip():
                                                arg = arg.replace("^", "**")
                                            
                                            variables = {}
                                            for variable in self.variables.keys():
                                                variables[variable] = self.variables[variable].literal
                                            
                                            eq = eval(arg.strip(), variables)
                
                                            if isinstance(eq, int):
                                                self.tokens["ARGS"].append(Tokens.Literals.Integer(eq))
                                            else:
                                                self.tokens["ARGS"].append(Tokens.Literals.Float(eq))
                                        except SyntaxError:
                                            if arg[0] == "$" and (arg[1] == "\"" and arg[-1] == "\""):
                                                self.tokens["ARGS"].append(Tokens.Literals.String(self.addVars(arg[1:-1])))
                                            else:
                                                isProc = False
                                                for returns in self.returns.keys():
                                                    if arg.strip()[:len(returns)] == returns:
                                                        isProc = True
                                                        proc = arg.strip()[:len(returns)]

                                                if isProc:
                                                    self.tokens["ARGS"].append(arg.strip())
                                                    self.tokens["LEXER"] = Lexer
                                                else:
                                                    self.error.print_stacktrace("LiteralError", f"Invalid literal '{arg.strip()}'")
                                        except NameError:
                                            self.error.print_stacktrace("VarError", f"Unknown variable '{arg.strip()}'")

            return self.tokens

        else:
            self.error.print_stacktrace("SyntaxError", "Missing parentheses")

    def addVars(self, string):
        for variable in self.variables.keys():
            if f"%{variable}%" in string:
                string = string.replace(f"%{variable}%", str(self.variables[variable].literal))

        return string[1:]