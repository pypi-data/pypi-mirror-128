
def _init_config():
	from .resource import Config

	return Config()

def _init_cache():
	from .resource import Cache

	return Cache()

config = _init_config()
cache = _init_cache()

from .notify import Notify
from .keyring import Keyring

from .keybinds import keybinds

from .state import Init

from .client_process import ClientProcess
from .server import Server
