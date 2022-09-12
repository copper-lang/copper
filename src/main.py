from utils.interpreter import Interpreter

print("Enter filepath:")
filepath = input(">>> ")

file = open(filepath, 'r')
lines = file.readlines()

for line in lines:
	if line[:2] == "//" or line == "\n":
		pass
	else:
		interpreter = Interpreter(line)
		interpreter.interpret()