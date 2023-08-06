
from collections import namedtuple

from . import config

_RofiKb = namedtuple('_RofiKb' , 'code name')

class Keybinds():

	__dump = {}
	__list = []

	DEFAULT = _RofiKb(1, None)
	CUSTOM  = _RofiKb(10, '-kb-custom-1')
	HIDDEN  = _RofiKb(11, '-kb-custom-2')
	ATTRS   = _RofiKb(12, '-kb-custom-3')

	@property
	def list(self):
		if (not self.__list):
			self.__list = [] \
				+ self._release(self._kb_hidden) \
				+ self._release(self._kb_custom) \
				+ self._release(self._kb_attrs) \
				\
				+ [self.HIDDEN.name, self._kb_hidden] \
				+ [self.CUSTOM.name, self._kb_custom] \
				+ [self.ATTRS.name, self._kb_attrs]

		return self.__list

	def _release(self, kb):
		result = []

		for name, keys in self._dump.items():
			if (kb in keys):
				keys.remove(kb)
				self._dump[name] = keys
				result = ['-' + name, ','.join(keys)]

		return result

	@property
	def _dump(self):
		if (not self.__dump):
			import subprocess
			r = subprocess.run(
				'rofi -dump-config',
				shell = True,
				text = True,
				capture_output = True
			)

			if (r.stdout):
				self.__dump = dict(
					filter(
						bool,
						map(
							self._dump_parser(),
							r.stdout.splitlines()
						)
					)
				)

		return self.__dump

	def _dump_parser(self):
		import re
		bind = re.compile(r'^(?:/\*)?\s+(kb-.+):\s+"(.+)"')
		def parse_dump(line):
			result = None

			match = bind.match(line)
			if (match):
				(name, keys) = match.groups()
				result = (name, keys.split(','))

			return result

		return parse_dump

	@property
	def _kb_hidden(self):
		return self._config.kb['hidden']

	@property
	def _kb_custom(self):
		return self._config.kb['custom_action']

	@property
	def _kb_attrs(self):
		return self._config.kb['pass_attrs']

	@property
	def _config(self):
		return config

keybinds = Keybinds()
