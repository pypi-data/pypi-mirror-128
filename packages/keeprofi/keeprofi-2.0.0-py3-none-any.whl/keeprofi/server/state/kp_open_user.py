
from hxss.responsibility import chain

from keeprofi import (
	Request,
	Response,
)
from keeprofi.server import Notify

from . import State
from . import KPOpen
from . import FSNavigation

class KPOpenUser(KPOpen):

	_up_str = '/..'

	def handle(self, request: Request) -> State:
		return chain(request) \
			| self._handle_up \
			| self._handle_pass \
			| chain

	def response(self) -> Response:
		return Response([self._up_str], 'pass: ', True)

	def _handle_up(self, request: Request) -> State:
		if (request.selection == self._up_str):
			return FSNavigation(self._path.parent)

	def _handle_pass(self, request: Request) -> State:
		connection = self._connect(request.selection)

		if (not connection):
			self._wrong_password()

		return connection

	def _wrong_password(self):
		Notify(
			'Wrong password',
			self._path.as_posix(),
			self._config.icons['fail']
		) \
			.show()
