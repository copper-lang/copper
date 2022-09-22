# Copper
Procedure-oriented programming language written in Python that focuses on data manipulation.

---

### Super Basic Docs
| Command | Purpose | Arguments | Example |
| :-------: | :-------: | :-------: | :------- |
| `out()` | Output text | string | `out("test")` |
| `in()` | Take in user input | string | `in("input: ")` |
| `set()` | Create a variable | variable name, literal (any type) | `set(name, "kryllyx")` |
| `cast()` | Convert variable to given type | variable name, type (`string`, `integer`, `float`, `boolean`) | `cast("16", integer)` |
| `round()` | Rounds a number | variable name, round type (`default`, `floor`) | `round(pi, floor)` |
||
| `proc()` | Defines a procedure | procedure name with parameters | <br><pre>proc(test(param))<br>    out(param)<br>endproc</pre> |
