from utils.objects.objects import Object

class Interpreter:
	def __init__(self, line):
		self.line = list(line)

	def interpret(self):
		if "".join(self.line)[:3] == "out":
			for char in "out":
				self.line.remove(char)

			if self.line[0] == "(" and self.line[-1] == ")":
				self.line.pop(0)
				self.line.pop()

				object = Object("".join(self.line))
				type = object.checkType()

				if type[0] == "string":
					print(type[1].string)