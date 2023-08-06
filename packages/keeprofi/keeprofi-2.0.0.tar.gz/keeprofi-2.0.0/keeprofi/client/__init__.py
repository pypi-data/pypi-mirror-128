
import asyncio
import sys
import os

from keeprofi import (
	APP_NAME,
	__SOCKET_ADDRESS as SOCKET_ADDRESS,
	__SOCKET_FAMILY as SOCKET_FAMILY,
	logger,
	Connection,
	Request,
	Response,
)

class Client():

	__connection = None

	async def connect(self, args):
		self.__connection = await Connection.create(
			asyncio.get_running_loop(),
			*await asyncio \
				.open_unix_connection(SOCKET_ADDRESS),
			self.__log
		)

		action = os.getenv('ROFI_RETV')
		selection = (args[0:] or [None])[0]
		self._write(Request(action, selection))

		response = await self._read() or Response([])
		print('\0prompt\x1f' + response.prompt + '\n')
		print('\0use-hot-keys\x1ftrue\n')
		print(
			'\0no-custom\x1f'
			+ str(not response.custom).lower()
			+ '\n'
		)

		for item in response.ls:
			print(item + '\n')

		self.close()

	async def _read(self):
		return await self.__connection.read()

	def _write(self, data):
		return self.__connection.write(data)

	def close(self):
		if (self.__connection):
			self.__connection.close()
			self.__connection = None

		self.__log('close')

	def __log(self, text):
		logger.debug('[client]: ' + str(text))

	def __del__(self):
		self.close()
