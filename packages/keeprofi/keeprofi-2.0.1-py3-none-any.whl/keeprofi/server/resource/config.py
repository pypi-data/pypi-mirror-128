
import os
from xdg import BaseDirectory
from pathlib import PosixPath

from keeprofi import APP_NAME
from .resource import Resource

class Config(Resource):
	ACTION_COPY: 'copy'
	ACTION_TYPE: 'type'

	@property
	def _defaults(self):
		return {
			'default_action': 'copy',
			'save_masterpass': False,
			'keybinds': {
				'hidden': 'Control+h',
				'custom_action': 'Control+Return',
				'pass_attrs': 'Shift+Return',
			},
			'notify_icons': {
				'success': 'keepassxc-dark',
				'fail': 'keepassxc-locked',
			},
			'dir_format': '/{name}'
		}

	@property
	def kb(self):
		return self.keybinds

	@property
	def icons(self):
		return self.notify_icons

	@property
	def _path(self):
		config_home = BaseDirectory.xdg_config_home

		return PosixPath(
			config_home \
			+ '/' \
			+ ('', '.')[
				int(os.environ['HOME'] == config_home)
			] \
			+ APP_NAME
			+ '/config.yaml'
		)

	def is_copy_default(self):
		consts = self.__class__.__dict__.get('__annotations__')

		return self.default_action == consts['ACTION_COPY']
