__version__ = '0.2.0'

try:
  import rich.traceback
  rich.traceback.install()
except ImportError:
  pass

from .core import *

from . import envs
from . import run
