
from __future__ import annotations

from keeprofi import (
	Request,
	Response,
)

class State():

	def handle(self, request: Request) -> State:
		raise NotImplementedError

	def response(self) -> Response:
		raise NotImplementedError
