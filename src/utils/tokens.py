from .literals.string import String

class Tokens:
	class Procs:
		class Builtins:
			class Output:
				pass

			class Input:
				pass

			class Variable:
				pass

	class Literals:
		class String(String):
			def __init__(self, string):
				super().__init__(string)