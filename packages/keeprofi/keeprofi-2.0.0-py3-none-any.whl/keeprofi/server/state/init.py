
from pathlib import PosixPath

from keeprofi import Request
from keeprofi.server import cache

from . import State
from . import KPOpenKeyring
from . import FSNavigation

class Init(State):

	def handle(self, request: Request) -> State:
		return (kdb := cache.get('last_file')) \
			and KPOpenKeyring(PosixPath(kdb)) \
				.handle(request) \
			or FSNavigation()
