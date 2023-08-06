
import subprocess
import re

from keeprofi import (
	Request,
	Response,
)
from keeprofi.server import (
	config,
	cache,
)

from . import State

class Navigation(State):

	_request = None
	__ls = None
	__ls_str = None

	def handle(self, request: Request) -> State:
		selection = self._normalize_selection(request)

		return self._handle(
			Request(
				int(request.action),
				selection
			)
		)

		return selection \
			and self._handle(
				Request(
					int(request.action),
					selection
				)
			) \
			or self

	def response(self) -> Response:
		return Response(self._ls_str, self._rofi_prompt)

	def _handle(self, request: Request) -> State:
		raise NotImplementedError

	def _new_ls(self):
		raise NotImplementedError

	def _normalize_selection(self, request: Request):
		result = None

		if (self._ls_str.count(request.selection)):
			i = self._ls_str.index(request.selection)
			result = self._ls[i]

		return result

	@property
	def _ls(self):
		if (not self.__ls):
			self.__ls = self._new_ls()
			self.__ls_str = None

		return self.__ls

	@property
	def _ls_str(self):
		if (not self.__ls_str):
			self.__ls_str = list(map(
				self._item2str,
				self._ls
			))

		return self.__ls_str

	def _item2str(self, item):
		return str(item)

	@property
	def _rofi_prompt(self):
		return 'entry: '

	@property
	def _up_str(self):
		return '..'

	@property
	def _config(self):
		return config

	@property
	def _cache(self):
		return cache


