import os
from utils.interpreter import Interpreter

print("Enter filepath:")
filepath = input(">>> ")

file = open("tests/" + filepath, 'r')
lines = file.readlines()
location = os.getcwd() + "/" + filepath

lineno = 1
for line in lines:
	if line[:2] == "//" or line == "\n":
		pass
	else:
		interpreter = Interpreter(line, lineno, location)
		interpreter.interpret()

	lineno += 1