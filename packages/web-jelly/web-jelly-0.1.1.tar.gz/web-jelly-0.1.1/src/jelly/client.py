import time, sys, logging, os

from .transport import MQTT
from .logger import JellyLogger, LoggingLevel
from .util import uid
from .session import JellySession

LOG = logging.getLogger(__name__)

class SessionHandler:
  def __init__ (self):
    self.process = None
    self.queue = None
    
class JellyClient:
  def __init__ (self, version='v1', host='ws.web-jelly.com', port=1883):
    self.version = version
    self.client_id = uid()    
    self.config = dict(
      host=host, port=port
    )

    self.transport = None    
    self.sessions = {}
    
  def session (self, scope):
    if not scope in self.sessions:
      self.sessions[scope] = JellySession(self, scope)
    return self.sessions[scope]
  
  def serve (self):
    while 1:
      time.sleep(0.1)
    
  def kill (self):
    self.transport.wait_for_publish()
    os._exit(0)
  
  def subscribe_broadcast (self):
    return self.transport.subscribe("%s/%s" % (self.version, 'broadcast'))

  def configure (self, **kw):
    self.config.update(**kw)
    self.transport = MQTT(self.config['host'], self.config['port'], self.client_id)
    app_path = os.path.abspath(self.config.get('app', '.'))
    sys.path.append(app_path)
    for id, session in self.sessions.items():
      session.configure(**kw)
    
  def publish (self, topic, msg):
    self.transport.publish(topic, msg)

  def subscribe (self, topic):
    return self.transport.subscribe(topic)


