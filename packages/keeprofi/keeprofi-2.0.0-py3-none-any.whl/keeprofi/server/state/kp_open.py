
from pathlib import PosixPath

from pykeepass import PyKeePass

from keeprofi.server import (
	config,
	cache,
	Keyring,
)

from . import State
from . import KPNavigation

class KPOpen(State):

	_keyring = Keyring()

	def __init__(self, path: PosixPath):
		self._path = path.resolve()

	def _connect(self, password) -> State:
		result = None

		try:
			connection = PyKeePass(
				self._path.as_posix(),
				password=password
			)

			self._keyring.save_pass(password)
			self._cache.last_file = self._path.as_posix()

			result = KPNavigation(connection.root_group)
		except Exception as e:
			pass

		return result

	@property
	def _config(self):
		return config

	@property
	def _cache(self):
		return cache
