
from pathlib import PosixPath
import subprocess

from hxss.responsibility import chain

from keeprofi import Request
from keeprofi.server import (
	state,
	keybinds,
)

from . import (
	State,
	Navigation,
)

class FSNavigation(Navigation, State):

	def __init__(self, cwd: PosixPath = None):
		self._cwd = cwd or PosixPath.home()

	def _handle(self, request: Request) -> State:
		return chain(request) \
			| self._handle_switch_hidden \
			| self._handle_chdir \
			| self._handle_kp \
			| chain

	def _handle_switch_hidden(self, request):
		if (request.action == keybinds.HIDDEN.code):
			self._switch_hidden()

			return FSNavigation(self._cwd)

	def _handle_chdir(self, request):
		if (request.selection.is_dir()):
			return FSNavigation(request.selection)

	def _handle_kp(self, request):
		return state.KPOpenKeyring(request.selection) \
			.handle(request)

	def _new_ls(self):
		return [self._cwd.joinpath(self._up_str)] \
			+ list(
				filter(
					self._filter_files,
					sorted(
						self._cwd.iterdir(),
						key = self._sort_key
					)
				)
			)

	def _sort_key(self, item):
		return str(1 * item.is_file()) + item.name

	def _filter_files(self, item):
		return item.is_dir() \
			and (
				self._show_hidden
				or not item.name.startswith('.')
			) \
			or item.name.endswith('.kdbx')

	def _item2str(self, item):
		return self._render_dir(item) or item.name

	def _render_dir(self, item):
		return item.is_dir() \
			and self._config.dir_format \
				.format(name = item.name) \
			or None

	def _switch_hidden(self):
		self._show_hidden = not self._show_hidden

	@property
	def _show_hidden(self):
		return self._cache.show_hidden_files

	@_show_hidden.setter
	def _show_hidden(self, show_hidden):
		self._cache.show_hidden_files = show_hidden

	@property
	def _rofi_prompt(self):
		return 'file: '
