import sys
from utils.lexer import Lexer

print("Enter filepath:")
filepath = input(">>> ")

try:
	file = open("tests/" + filepath, 'r')
except FileNotFoundError:
	print(f"\n\033[0;31mUnknownFileError: Could not find the file '{filepath}'\033[0;0m\n")
	sys.exit()
else:
	lines = file.readlines()

	lineno = 1
	for line in lines:
		lexer = Lexer(line)
		lexer.lex()
		
		lineno += 1