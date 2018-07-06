# Lis.py

This project is a small Scheme interpreter
written in Python based on the implentation
in [this article](http://norvig.com/lispy.html).

You can run a Scheme REPL with the command `python lis.py`.

So far this intepreter is just an implementation
of the the code in the article, but I may
add on more features as time goes on for exercise.

### Features include:
- Numeric data types (int and float)
- `define` keyword to define global variables
- `set!` keyword to change the value of previously defined variables
- `lambda` keyword for function expressions
- `if` keyword for conditional expressions

### Missing features
- `let` keyword to define local variables in function definitions
- `cond` keyword for multi-condition expressions
- Missing tail recursion
- Missing other data types (string, char, boolean, vectors)
- No error recovery
