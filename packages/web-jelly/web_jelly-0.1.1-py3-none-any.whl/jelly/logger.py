import inspect, time, sys, builtins, logging, traceback, re, hashlib, weakref
from .util import (
  is_iterable, is_primitive, is_dict, is_instance, is_iterable,
  is_module, is_builtin, uid, now, function_name, getpath, object_key
)

LOG = logging.getLogger(__name__)

TYPE_KEY = '__type__'
EXIST_KEY = '__exist__'

class TYPE:
  LOG='LOG'
  EVENT='EVENT'
  OBJECT='OBJECT'

class LoggingLevel:
  STATUS = 60
  CRITICAL = 50
  ERROR = 40
  WARNING = 30
  INFO = 20
  DEBUG = 10
  NOTSET = 0

def log_level_name (level):
  if level == LoggingLevel.STATUS:
    return 'STATUS'
  elif level == LoggingLevel.CRITICAL:
    return 'CRITICAL'
  elif level == LoggingLevel.ERROR:
    return 'ERROR'
  elif level == LoggingLevel.WARNING:
    return 'WARNING'
  elif level == LoggingLevel.INFO:
    return 'INFO'
  elif level == LoggingLevel.NOTSET:
    return 'NOTSET'
  return ''

def get_level (name):
  for k, v in LoggingLevel.__dict__.items():
    if k == name:
      return v
  return LoggingLevel.NOTSET

class LogType:
  LOG=0
  EVENT=1

class JellyfishLoggingHandler(logging.NullHandler):
  def __init__ (self, client):
    super(JellyfishLoggingHandler, self).__init__()
    self.client = client
    
  def emit(self, record):
    publish_logging_record(self.client, record)


def create_stack (stack):
  info = inspect.getinnerframes(stack)
  stack_data = []
  for frame in info:
    frame_data = {
      'source': '' if not frame.code_context else ''.join(list(frame.code_context)),
      'line': frame.lineno, 'file': frame.filename, 'function': frame.function
    }
    stack_data.append(frame_data)
  return stack_data

def publish_logging_record (client, record):
  if record.name.startswith('jelly'):
    return
  
  record.levelname = log_level_name(record.levelno)
  message = record.getMessage()
  try:
    stack = None
    log_type = LogType.LOG
    log_hash = None
    msg = record.msg
    args = record.args
    
    if record.exc_info:
      exc = traceback.format_exception(*record.exc_info)
      exception = record.exc_info[1]
      exc_class = record.exc_info[0]
      msg = "%s: %s" % (exc_class.__name__, str(exception)) # ''.join(exc)
      log_type = LogType.EVENT
      stack = create_stack(record.exc_info[2])
      hash_value = exc_class.__name__ + ':' + '-'.join([s['source'] for s in stack])
      
      hash_object = hashlib.md5(hash_value.encode())
      log_hash = str(hash_object.hexdigest())
      args = [{
        TYPE_KEY: TYPE.EVENT, 'id': log_hash, 'message': msg, 'details': {}
      }]
      
    elif not isinstance(msg, str):
      args = [msg]
      msg = "%s"
    
    if args and not isinstance(args, (tuple, list,)):
      args = [args]  
    items = [client.serializer.serialize(arg) for arg in args]
    
    shape = "%s:%s:%s:%s:%s" % (
      len(message), len(list(re.finditer("\r\n?|\n", message))),
      len(msg), len(list(re.finditer("\r\n?|\n", message))),
      len(args)
    )
    client.publish_log(dict(__type__=TYPE.LOG,
      task=record.extra.get('task'),
      name=record.name, msg=msg, level=record.levelname,
      levelno=record.levelno, ts=time.time()*1000.0,
      thread=record.thread, threadName=record.threadName,
      process=record.process, module=record.module,
      lineno=record.lineno, pathname=record.pathname,
      args=items, message=message, shape=shape,
      stack=stack, type=log_type, hash=log_hash
    ))
  except Exception as err:
    LOG.error('failed to parse log: %s', err)

class TaskLogger:
  def __init__ (self, logger, id=None, total=0, completed=0):
    self.logger = logger
    self.id = id or uid()
    self.total = total
    self.completed = completed

  def log (self, level, msg, *args, **kwargs):
    kwargs.setdefault('extra', {})
    if 'completed' in kwargs:
      self.completed = kwargs['completed']
    kwargs['extra']['task'] = dict(
      id=self.id, completed=self.completed, total=self.total
    )
    self.logger.log(level, msg, *args, **kwargs)

  def info (self, msg, *args, **kwargs):
    self.log(LoggingLevel.INFO, msg, *args, **kwargs)
  def error (self, msg, *args, **kwargs):
    self.log(LoggingLevel.ERROR, msg, *args, **kwargs)
  def debug (self, msg, *args, **kwargs):
    self.log(LoggingLevel.DEBUG, msg, *args, **kwargs)
  def warn (self, msg, *args, **kwargs):
    self.log(LoggingLevel.WARNING, msg, *args, **kwargs)


def object_ref (obj):
  return {'id': str(id(obj)), 'class': type(obj).__name__}

class JellyLogger:

  def __init__ (self, client):
    self.client = client
    self.active_request = None
    self.level = LoggingLevel.NOTSET
    self.current_print_line = None
    self.serializer = ObjectSerializer()

  def task (self, logger, id=None, completed=None, total=None):
    return TaskLogger(logger, id=id, completed=completed, total=total)


  def inspect (self, object=None, paths=None):
    if not object:
      objects = self.serializer.list_objects()
      return {
        EXIST_KEY: True, 
        'objects': [object_ref(obj) for obj in objects]
      }
    
    inst = self.serializer.get_object(object)
    if not inst:
      return {EXIST_KEY: False, 'object': object}

    if not paths:
      return {EXIST_KEY: True, 'object': object, 'value': self.serializer.serialize(inst)}

    result = {
      EXIST_KEY: True, 'object': object, 'values': {}
    }
    for path in paths:
      try:
        value = getpath(inst, path)
        result['values'][path] = {
          EXIST_KEY: True, 'value': self.serializer.serialize(value)
        }
      except:
        result['values'][path] = {EXIST_KEY: False}
    return result

  def activate (self, level=LoggingLevel.DEBUG):
    # NOTE:
    #   for some reason, adding a handler messes with basicConfig somehow
    #   have to use logging factory to intercept logs 
    self.level = get_level(level)
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
      record = old_factory(*args, **kwargs)
      if not hasattr(record, 'extra'):
        record.extra = {}
      record.extra.update(**kwargs.get('extra', {}))
      publish_logging_record(self, record)
      return record
    logging.setLogRecordFactory(record_factory)
    
    print_logger = logging.getLogger('print')
    def new_print (*args, **kwargs):
      end = kwargs.get('end')
      log_msg = " ".join(["%s" for _ in range(len(args))])
      print_logger.info(log_msg, *args)
    
    old_excepthook = sys.excepthook
    def excepthook (exc_type, exc_value, exc_traceback):
      if exc_type is not KeyboardInterrupt:
        logging.error('', exc_info=(exc_type, exc_value, exc_traceback))
      old_excepthook(exc_type, exc_value, exc_traceback)
    sys.excepthook = excepthook
    #builtins.print = new_print    
    
    # NOTE: do not do this: (test with basicConfig)
    # logging.root.addHandler(JellyfishLoggingHandler(self))
    
  def publish_log (self, log):
    level = log.get('levelno')
    log_level = self.level
    if not isinstance(level, int) or not isinstance(log_level, int):
      return
    if log_level <= level:
      log['_id'] = str(uid())
      try:
        self.client.publish('log', log, log['type'], log['levelno'])
      except Exception as err:
        LOG.error('failed to publish log: %s', err)

  def set_active_request (self, req_id):
    self.active_request = req_id

  

class ObjectSerializer:
  def __init__ (self):
    self._objects = {}

  def _register (self, obj):
    try:
      obj_key = object_key(obj)
      if obj_key not in self._objects:
        self._objects[obj_key] = weakref.ref(obj, self._on_object_deleted)
    except Exception as err:
      LOG.error('failed to register object: %s', obj)

  def _on_object_deleted (self, obj):
    pass

  def get_object (self, obj_id):
    obj = self._objects[obj_id]
    if obj:
      return obj.ref()
    return obj

  def serialize (self, value):
    result = None
    if is_primitive(value):
      result = value
    elif is_dict(value):
      result = {k: self.serialize(v) for k, v in value.items()}
    elif is_iterable(value):
      result = [self.serialize(v) for v in value]
    elif hasattr(value, '__serialize__'):
      result = value.__serialize__(self.serialize)
    elif is_instance(value) and hasattr(value, '__event__'):
      result = {
        TYPE_KEY: TYPE.EVENT
      }
      result.update(**value.__event__())      
    #elif isinstance(value, Exception):
    #  result = {
    #    TYPE_KEY: 'event'
    #  }
    #  message = type(value).__name__ + ': ' + str(value)
    #  result.update(**dict(
    #    message=message,
    #    id=message, level=LoggingLevel.ERROR
    #  ))
    elif is_instance(value):
      if not isinstance(value, Exception):
        self._register(value)
      state = {}
      result = {TYPE_KEY: TYPE.OBJECT}
      if hasattr(value, '__state__'):
        state = self.serialize(value.__state__())
      result.update(**{
        'class': type(value).__name__,
        'id': object_key(value),
        'message': str(value),
        'state': state
      })
    else:
      result = {TYPE_KEY: 'unknown'}
    return result
