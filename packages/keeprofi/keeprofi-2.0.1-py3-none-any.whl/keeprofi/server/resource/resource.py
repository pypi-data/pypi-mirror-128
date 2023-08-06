
import yaml
from yaml import Loader

from pathlib import PosixPath

from keeprofi import logger

class Resource():

	def __init__(self):
		self._dict = self._defaults
		self.get = self._dict.get
		self.create()
		self.load()
		self._switch_dict()

	def create(self):
		self._path.parent.mkdir(
			parents = True,
			exist_ok = True
		)

		if (
			not self._path.is_file()
			or not self._path.stat().st_size
		):
			self.save()

	def save(self):
		with self._path.open('w', encoding='utf-8') as file:
			yaml.dump(
				self._dict,
				file,
				sort_keys = False,
			)

	def load(self):
		if (self._path.is_file()):
			with self._path.open('r') as file:
				try:
					self._dict |= yaml.load(file, Loader = Loader)
				except Exception as e:
					logger.warning(
						'Error loading: '
						+ self._path.resolve().as_posix()
					)

	def _switch_dict(self):
		self.__setattr = self._dict.__setitem__

	@property
	def _defaults(self):
		return {}

	@property
	def _path(self) -> PosixPath:
		raise NotImplementedError

	def __getattr__(self, name):
		if (name in self._dict):
			return self._dict[name]

		raise AttributeError(name)

	def __setattr__(self, name, value):
		self.__setattr(name, value)

	def __setattr(self, name, value):
		self.__dict__[name] = value

	def __delattr__(self, name):
		if (name in self._dict):
			del self._dict[name]
		else:
			raise AttributeError(name)
