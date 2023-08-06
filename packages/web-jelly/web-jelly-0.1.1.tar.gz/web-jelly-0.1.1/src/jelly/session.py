import multiprocessing, logging, platform, threading, time
from .logger import JellyLogger, LoggingLevel

LOG = logging.getLogger(__name__)
ENV = multiprocessing.get_context("spawn")

def evaluate_script (session):
  _globals = {}
  _globals.update(**globals())
  _globals.update(
    info=logging.info, debug=logging.debug, error=logging.error
  )
  scope = {}
  code = session.get('code', '')
  try:
    exec(code, _globals, scope)
    if '__main__' in scope:
      scope['__main__']()
  except Exception as err:
    #LOG.error("%s", err)
    LOG.exception(err)
  finally:
    pass
    #LOG.log(LoggingLevel.STATUS, 'evaluate complete')

def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

def os_information ():
  return dict(
    python_version=platform.python_version(),
    libc_version='-'.join(platform.libc_ver()),
    node=platform.node(),
    linux_distribution=linux_distribution(),
    system=platform.system(),
    release=platform.release(),
    machine=platform.machine(),
    platform=platform.platform(),
    version=platform.version(),
  )

class JellySession:
  def __init__ (self, client, scope):
    self.client = client
    self.scope = scope.lower()
    self.model = {}
    self.config = {}
    self.configured = False
    self.logging = JellyLogger(self)
    self.rpc = JellyRPC(self)
    
  #def inspect (self, object=None, paths=None):
  #  data = self.logging.inspect(object=object, paths=paths)
  #  if data:
  #    self.publish('inspect', data)
  
  
  def publish (self, method, payload, *args):
    topic = self.make_topic(method, args=list(args))
    payload.update(scope=self.scope)
    LOG.debug("%s -> %s", self.scope, topic)
    self.client.publish(topic, payload)

  def configure (self, **config):
    self.config = config
    self.logging.activate(**config.get('logging', {}))
    self.rpc.activate(**config.get('rpc', {}))
    self.introduce()
    LOG.info('process started: %s', self.scope)
    self.configured = True

  def subscribe_method (self, method):
    topic = self.make_topic(method, 'inbox')
    return self.client.subscribe(topic)
  
  def introduce (self):
    self.publish('status', dict(
      system=os_information(),
      metadata=self.config.get('metadata', {})
    ))

  def make_topic (self, method, group='outbox', args=None):
    user_type = 'client'
    rest = '' if not args else ('/' + '/'.join(map(str, args)))
    topic = "%s/%s/%s/%s/%s/%s%s" % (
      self.client.version, group, user_type, self.client.client_id, 
      self.scope, method, rest
    )
    return topic.lower()

  def set_model (self, model):
    if self.model == model:
      LOG.debug('no changes in session, skipping: %s', model['id'])
      return
    LOG.debug('session model updated')
    self.model = model
    if not self.configured:
      self.configure(**self.config)
    evaluate_script(model)
    #if self.process:
    #  self.process.kill()
    #self.queue = ENV.Queue()
    #self.process = ENV.Process(target=evaluate_script, args=(self.queue, session))
    #self.process.start()
    
  def evaluate (self, code):
    pass
    #LOG.log(LoggingLevel.STATUS, 'starting evaluate')
    
  def register_session (self, model):
    session = self.client.session(model['scope'])
    if session is self:
      return
    session.config = self.config.copy()
    session.set_model(model)
    
  def subscribe_broadcast (self):
    return self.client.subscribe_broadcast()


# == RPC ==
class Action:
  def __init__ (self, client, action_id, handler):
    self.client = client
    self.id = action_id
    self.handler = handler
  
  def execute (self, param):
    self.client.execute_action(self.id, self.handler, param)

class JellyRPC:
  def __init__ (self, session):
    self.session = session
    self.active_calls = {}
    self.commands = {}
    self._main_thread = None
    
  def set_command (self, name, args, handler):
    self.commands[name] = dict(
      args=args, handler=handler
    )

  def activate (self, **kwargs):
    self._main_thread = threading.Thread(target=self._main_loop)
    self._main_thread.daemon = True
    self._main_thread.start()

  def _main_loop (self):
    requests = self.session.subscribe_method('rpc')
    broadcasts = self.session.subscribe_broadcast()
    while 1:
      for breq in broadcasts:
        self.session.introduce()
      for req in requests:
        try:
          self._handle_request(req)
        except Exception as err:
          LOG.exception(err)
      time.sleep(0.01)

  def _handle_request (self, req):
    LOG.info('handle request: %s, %s', self.session.scope, req.payload)
    type = req.payload.get('type', '').lower().strip()
    args = req.payload.get('payload', {})
    cmd = self.commands.get(type)
    if type == '__session__':
      self.session.register_session(args)      
    #elif type == '__inspect__':
    #  self.session.inspect(**args)
    elif not cmd:
      raise RuntimeError('no such command: %s' % type)
    else:
      cmd['handler'](**args)
    