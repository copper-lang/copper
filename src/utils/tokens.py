from .literals.string import String
from .literals.integer import Integer
from .literals.float import Float
from .literals.boolean import Boolean

class Tokens:
	class Procs:
		class Builtins:
			class Output: pass
			class Input: pass
			class Variable: pass
			class Cast: pass

	class Literals:
		class String(String):
			def __init__(self, string):
				super().__init__(string)

		class Integer(Integer):
			def __init__(self, integer):
				super().__init__(integer)

		class Float(Float):
			def __init__(self, decimal):
				super().__init__(decimal)

		class Boolean(Boolean):
			def __init__(self, boolean):
				super().__init__(boolean)