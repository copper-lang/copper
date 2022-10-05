import sys, os
from utils.lexer import Lexer
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

	for line in lines:
		error = Error(
			line,
			lineno,
			location
		)
		
		lexer = Lexer(line, error)
		tokens = lexer.lex()
		
		lineno += 1