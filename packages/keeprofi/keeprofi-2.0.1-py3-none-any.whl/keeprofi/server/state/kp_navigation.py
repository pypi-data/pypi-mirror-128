
from pathlib import PosixPath

import xerox
from pykeepass import PyKeePass
from pykeepass.group import Group
from pykeepass.entry import Entry
from pynput.keyboard import Controller
from hxss.responsibility import chain

from keeprofi import Request
from keeprofi.server import (
	Notify,
	keybinds,
)

from . import State
from . import Navigation
from . import FSNavigation

class KPNavigation(Navigation, State):

	def __init__(self, group: Group):
		self._group = group

	def _handle(self, request: Request) -> State:
		return chain(request) \
			| self._handle_up \
			| self._handle_chgroup \
			| self._handle_action \
			| chain

	def _handle_up(self, request):
		if (request.selection == self._group):
			delattr(self._cache, 'last_file')

			return FSNavigation(
				PosixPath(self._group._kp.filename).parent
			)

	def _handle_chgroup(self, request):
		if (isinstance(request.selection, Group)):
			return KPNavigation(request.selection)

	def _handle_action(self, request):
		return {
			keybinds.DEFAULT.code: self._default_action,
			keybinds.CUSTOM.code:  self._custom_action,
			keybinds.ATTRS.code:   self._navigate_entry,
		}[int(request.action)](request.selection)

	def _default_action(self, selection):
		return (
			self._type_pass,
			self._copy_pass,
		)[self._config.is_copy_default()](selection)

	def _custom_action(self, selection):
		return (
			self._copy_pass,
			self._type_pass,
		)[self._config.is_copy_default()](selection)

	def _copy_pass(self, selection):
		xerox.copy(selection.password)
		Notify(
			'Password copied',
			self._entry_title(selection),
			self._config.icons['success']
		).show()

		return None

	def _type_pass(self, selection):
		Controller().type(selection.password)

		return None

	def _navigate_entry(self, selection):
		from . import KPEntryNavigation

		return KPEntryNavigation(selection)

	def _new_ls(self):
		return [self._parentgroup()] \
			+ sorted(
				self._group.subgroups,
				key = lambda g: g.name
			) \
			+ sorted(
				self._group.entries,
				key = self._entry_title
			)

	def _parentgroup(self):
		group = self._group.parentgroup or self._group
		group.name = self._up_str

		return group

	def _item2str(self, item):
		return isinstance(item, Group) \
			and '/' + item.name \
			or self._entry_title(item)

	def _entry_title(self, entry):
		return entry.title \
			or entry.username \
			or entry.url \
			or 'Entry#' + entry.uuid

	@property
	def _rofi_prompt(self):
		return 'kbd: '
