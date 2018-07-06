"""
Lis.py Scheme Interpreter
-------------------------
Source code for a simple Scheme
interpreter based on the article:

http://norvig.com/lispy.html

"""


import math
import operator as op


def tokenize(chars):
  """
  Split a string of characters into tokens

  """
  return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def atom(token):
  """
  Convert numeric symbols to number types,
  everything else is left as a string

  """
  try:
    return int(token)
  except ValueError:
    try: return float(token)
    except ValueError:
      return str(token)


def read_from_tokens(tokens):
  """
  Generate the syntax tree from a list
  of tokens

  """
  if len(tokens) == 0:
    raise SyntaxError('Unexpected EOF')
  token = tokens.pop(0)
  if token == '(':
    L = []
    while tokens[0] != ')':
      L.append(read_from_tokens(tokens))
    tokens.pop(0) # pop the last ')'
    return L
  elif token == ')':
    raise SyntaxError('Unexpected )')
  else:
    return atom(token)


def parse(program):
  """
  Generate syntax tree from a
  program string

  """
  return read_from_tokens(tokenize(program))


class Env(dict):
  """
  An environment class with key-value pairs
  and an outer environment

  """
  def __init__(self, params=(), args=(), outer=None):
    self.update(zip(params, args))
    self.outer = outer

  def find(self, var):
    """
    Find the innermost environment where
    var occurs

    """
    return self if (var in self) else self.outer.find(var)


class Prodecure(object):
  """
  A user-defined Scheme procedure

  """
  def __init__(self, params, body, env):
    self.params, self.body, self.env = params, body, env

  def __call__(self, *args):
    """
    When a procedure is called it instantiates
    its own local environment which sets local
    variables not accessible outside the body of
    the function

    """
    return eval(self.body, Env(self.params, args, self.env))


def standard_env():
  """
  Defines the standard environmental
  variables which the interpreter
  will use to evaluate expressions

  """
  env = Env()
  env.update(vars(math))
  env.update({
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    '>': op.gt,
    '<': op.lt,
    '>=': op.ge,
    '<=': op.le,
    '=': op.eq,
    'abs': abs,
    'append': op.add,
    'apply': lambda proc, args: proc(*args),
    'begin': lambda *x: x[-1],
    'car': lambda x: x[0],
    'cdr': lambda x: x[1:],
    'cons': lambda x, y: [x] + y,
    'eq?': op.is_,
    'expt': pow,
    'equal?': op.eq,
    'length': len,
    'list': lambda *x: list(x),
    'list?': lambda x: isinstance(x, list),
    'map': map,
    'max': max,
    'min': min,
    'not': op.not_,
    'null?': lambda x: x == [],
    'number?': lambda x: isinstance(x, int) or isinstance(x, float),
    'procedure?': callable,
    'round': round,
    'symbol?': lambda x: isinstance(x, str),
  })
  return env


global_env = standard_env()


def eval(x, env=global_env):
  """
  Evaluates a given expression (x) after
  it has been tokenized and the syntax
  tree has been constructed

  """
  if isinstance(x, str):
    return env.find(x)[x]
  elif not isinstance(x, list):
    return x
  op, args = x[0], x[1:]
  if op == '\'': # quote
    return args[0]
  elif op == 'if':
    test, conseq, alt = args
    exp = (conseq if eval(test, env) else alt)
    return eval(exp, env)
  elif op == 'define':
    symbol, exp = args
    env[symbol] = eval(exp, env)
  elif op == 'set!':
    symbol, exp = args
    env.find(symbol)[symbol] = eval(exp, env)
  elif op == 'lambda':
    params, body = args
    return Prodecure(params, body, env)
  else:
    proc = eval(op, env)
    vals = [eval(arg, env) for arg in args]
    return proc(*vals)


def schemestr(exp):
  """
  Convert a Python object back into a
  Scheme-readable string

  """
  if isinstance(exp, list):
    return '(' + ' '.join(map(schemestr, exp)) + ')'
  else:
    return str(exp)


def repl(prompt='lis.py> '):
  """
  Read-eval-print-loop

  """
  while True:
    val = eval(parse(raw_input(prompt)))
    if val is not None:
      print schemestr(val)


repl()
