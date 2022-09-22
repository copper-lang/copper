import os, sys
from utils.interpreter import Interpreter

print("Enter filepath:")
filepath = input(">>> ")

try:
	file = open("tests/copper/" + filepath, 'r')
except FileNotFoundError:
	print(f"\n\033[0;31mUnknownFileError: Could not find the file '{filepath}'\033[0;0m\n")
	sys.exit()
else:
	lines = file.readlines()
	location = os.getcwd() + "/" + filepath

	lineno = 1
	variables = {}
	functions = {}
	isFunction = False
	function = ""
	for line in lines:
		if line[:2] == "//" or line == "\n":
			pass
		else:
			interpreter = Interpreter(line.strip(), variables, functions, isFunction, function, lineno, location)
			variables, functions, isFunction, function = interpreter.interpret()
	
		lineno += 1
