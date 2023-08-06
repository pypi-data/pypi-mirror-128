
from keeprofi import Request

from . import State
from . import KPOpen
from . import KPOpenUser

class KPOpenKeyring(KPOpen):

	def handle(self, request: Request) -> State:
		password = self._keyring.get_pass()

		return password \
			and self._connect(password) \
			or KPOpenUser(self._path)
