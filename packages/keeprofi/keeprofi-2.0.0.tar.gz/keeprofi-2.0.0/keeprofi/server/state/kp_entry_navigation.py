
import xerox
from pykeepass import PyKeePass
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
from . import KPNavigation

class KPEntryNavigation(Navigation, State):

	def __init__(self, entry: Entry):
		self._entry = entry

	def _handle(self, request: Request) -> State:
		return chain(request) \
			| self._handle_up \
			| self._handle_action \
			| chain

	def _handle_exit(self, request):
		return request.action == 1 or None

	def _handle_up(self, request):
		if (request.selection == self._up_str):
			return KPNavigation(self._entry.group)

	def _handle_action(self, request):
		return {
			keybinds.DEFAULT.code: self._default_action,
			keybinds.CUSTOM.code:  self._custom_action,
		}[request.action](request.selection)

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
		xerox.copy(self._value(selection))
		Notify(
			'Password attribute copied',
			self._entry.title + '.' + selection,
			self._config.icons['success']
		).show()

		return None

	def _type_pass(self, selection):
		Controller().type(self._value(selection))

		return None

	def _value(self, selection):
		return hasattr(self._entry, selection) \
			and getattr(self._entry, selection) \
			or self._entry.custom_properties[selection]

	def _new_ls(self):
		return [self._up_str] \
			+ list(filter(
				lambda attr: getattr(self._entry, attr),
				[
					'password',
					'username',
					'url',
					'notes',
					'tags',
				]
			)) \
			+ list(self._entry.custom_properties.keys())

	@property
	def _rofi_prompt(self):
		return 'entry: '

	@property
	def _up_str(self):
		return '/..'
