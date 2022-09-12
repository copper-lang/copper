from utils.objects.string import String

class Object:
	def __init__(self, object):
		self.object = object

	def checkType(self):
		if self.object[0] == "\"" and self.object[-1] == "\"":
			self.object = list(self.object)
			self.object.pop(0)
			self.object.pop()

			string = String("".join(self.object))
			return "string", string