import time
from collections.abc import Iterable

PRIMITIVE_TYPES = ['int', 'str', 'bool', 'float', 'long', 'NoneType']

def is_primitive (value):
  return type(value).__name__ in PRIMITIVE_TYPES

def is_iterable (value):
  return isinstance(value, Iterable)

def is_list (value):
  return isinstance(value, list) or isinstance(value, tuple)

def is_dict (value):
  return isinstance(value, dict)

def is_module (value):
  return type(value).__name__ == 'module'

def is_builtin (value):
  return is_primitive(value) or is_iterable(value) or is_dict(value) or is_module(value)

def is_instance (value):
  return not is_builtin(value)

def flatten (alist, result=None):
  if result is None:
    result = []
  for item in alist:
    if is_list(item):
      flatten(item, result)
    elif is_primitive(item):
      result.append(item)
    else:
      raise Exception('cannot flatten type: ' + type(item).__name__)
  return result

from uuid import uuid4
def now ():
  return int(time.time() * 1000)

def uid ():
  return str(uuid4())

def function_name (fn):
  klass = fn.__self__.__class__.__name__
  return "%s.%s" % (klass, fn.__name__)

def getpath (obj, path):
  if isinstance(path, str):
    path = path.split('.')
  result = obj
  for p in path:
    if is_instance(result):
      result = getattr(result, p)
    elif is_dict(result):
      result = result[p]
    elif is_iterable(result):
      result = result[int(p)]
    else:
      raise ValueError('%s does not exist' % p)
  return result

__ID__ = '__id__'
def object_key (obj):
  if hasattr(obj, __ID__):
    result = getattr(obj, __ID__)
    if callable(result):
      return str(result())
    return str(result)
  return str(id(obj))

