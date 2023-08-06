
import os
from xdg import BaseDirectory
from pathlib import PosixPath

from keeprofi import APP_NAME
from .resource import Resource

class Cache(Resource):

	@property
	def _defaults(self):
		return {
			'show_hidden_files': False,
			'keyring_timestamp': 0,
		}

	@property
	def _path(self):
		data_home = BaseDirectory.xdg_data_home

		return PosixPath(
			data_home \
			+ '/' \
			+ ('', '.')[
				int(os.environ['HOME'] == data_home)
			] \
			+ APP_NAME
			+ '/cache.yaml'
		)

	def __del__(self):
		self.save()
