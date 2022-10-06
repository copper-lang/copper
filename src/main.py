import sys, os
from utils.lexer import Lexer
from utils.interpreter import Interpreter
from utils.error import Error

print("Enter filepath:")
filepath = input(">>> ")

try:
	file = open("tests/" + filepath, 'r')
except FileNotFoundError:
	print(f"\n\033[0;31mUnknownFileError: Could not find the file '{filepath}'\033[0;0m\n")
	sys.exit()
else:
	lines = file.readlines()
	location = os.getcwd() + "/" + filepath
	lineno = 1

	variables = {}

	for line in lines:
		if line == "\n" or line[:2] == "//":
			pass
		else:
			error = Error(
				line,
				lineno,
				location
			)
	
			lexer = Lexer(line, error)
			tokens = lexer.lex()
	
			interpreter = Interpreter(tokens, variables, error)
			variables = interpreter.interpret()

		lineno += 1

	print(variables)