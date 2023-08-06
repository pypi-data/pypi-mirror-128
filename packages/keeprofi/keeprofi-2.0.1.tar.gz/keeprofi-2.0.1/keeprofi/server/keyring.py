
import keyring
import re

from datetime import (
	datetime,
	timedelta
)

from keeprofi import APP_NAME

from . import (
	config,
	cache
)

class Keyring():

	PASS_NAME = 'masterpass'

	def __init__(self):
		self._save = config.save_masterpass
		self._check_pass()

	def get_pass(self):
		return self._save \
			and keyring.get_password(
				APP_NAME,
				self.PASS_NAME
			) \
			or None

	def save_pass(self, password: str):
		if (self._save):
			keyring.set_password(
				APP_NAME,
				self.PASS_NAME,
				password
			)

			self._timestamp = datetime.now().timestamp()

	def _check_pass(self):
		if (not self._save or not self._is_actual()):
			self._delete_pass()

	def _delete_pass(self):
		self._timestamp = 0

		try:
			keyring.delete_password(
				APP_NAME,
				self.PASS_NAME
			)
		except Exception as e:
			pass

	def _is_actual(self):
		now = datetime.now()
		passdt = datetime.fromtimestamp(
			self._timestamp
		)

		return now - passdt <= self._delta

	@property
	def _delta(self) -> timedelta:
		if (not hasattr(self, '__delta')):
			self.__delta = timedelta()

			if (isinstance(self._save, str)):
				match = re.match(
					r'^(?:(\d+)W)?(?:(\d+)D)?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)??$',
					self._save
				)
				self.__delta = timedelta(
					weeks   = int(match.group(1) or 0),
					days    = int(match.group(2) or 0),
					hours   = int(match.group(3) or 0),
					minutes = int(match.group(4) or 0),
					seconds = int(match.group(5) or 0)
				)

		return self.__delta

	@property
	def _timestamp(self):
		return cache.keyring_timestamp

	@_timestamp.setter
	def _timestamp(self, timestamp: float):
		cache.keyring_timestamp = timestamp
