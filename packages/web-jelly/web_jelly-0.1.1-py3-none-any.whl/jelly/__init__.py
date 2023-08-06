import logging
from .client import JellyClient

LOG = logging.getLogger(__name__)
LOG.propagate = False

global __jelly__
__jelly__ = None
def init (*path, **config):
  global __jelly__
  route = []
  for p in path:
    if not isinstance(p, str):
      raise ValueError('path arguments must be string')
    for r in p.split('/'):
      if r:
        route.append(r)
  
  if not __jelly__:
    __jelly__ = JellyClient()
  
  scope = '.'.join(route[:3])
  __jelly__.session(scope)
  if config:
    __jelly__.configure(**config)
  return __jelly__

def serve ():
  global __jelly__
  __jelly__.serve()

def render (obj):
  global __jelly__
  __jelly__.render(obj)

