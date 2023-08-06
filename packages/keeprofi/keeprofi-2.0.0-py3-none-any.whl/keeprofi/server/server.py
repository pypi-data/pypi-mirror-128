
import asyncio
import signal
import sys

from multiprocessing.connection import Listener
from array import array

from keeprofi import (
	APP_NAME,
	__SOCKET_ADDRESS as SOCKET_ADDRESS,
	__SOCKET_FAMILY as SOCKET_FAMILY,
	__ARG_CLIENT as ARG_CLIENT,
	logger,
	Connection,
	Request,
	Response,
)

from . import (
	keybinds,
	Init,
	ClientProcess,
)

class Server():

	__loop = None
	__future = None
	__connection = None
	__process = None

	def __init__(self):
		self.state = Init()

	async def start(self):
		self.__loop = asyncio.get_running_loop()
		self.__loop.set_exception_handler(
			self._exception_handler
		)

		for signame in {'SIGINT', 'SIGTERM'}:
			self.__loop.add_signal_handler(
				getattr(signal, signame),
				self.stop
			)

		self.__loop.create_task(self.__listen_loop())
		self.__loop.create_task(self.__run_client())

		self.__future = self.__loop.create_future()
		await self.__future

	async def __listen_loop(self):
		self.__server = await asyncio.start_unix_server(
			self.__connected,
			SOCKET_ADDRESS,
		)

	async def __connected(self, reader, writer):
		self.__connection = await Connection.create(
			self.__loop,
			reader,
			writer,
			self.__log
		)

		self.__log('connected')

		request = await self._read()
		response = self._handle(request)

		self.__log('received')
		self.__log((request.action, request.selection))

		self.__log('response')
		self.__log(response.ls)

		(temp, self.__future) = response.custom \
			and (self.__future, self.__loop.create_future())  \
			or (None, self.__future)

		self.__log('sent')
		self._write(response)

		if (temp):
			self.stop()
			await self.__future
			self.__future = temp
			self._handle_pass(response)

	def _handle_pass(self, response: Response):
		import subprocess
		process = subprocess.run(
			[
				'rofi',
				'-dmenu',
				'-password',
				'-p',
				response.prompt,
			],
			input = '\n'.join(response.ls),
			text = True,
			capture_output = True
		)

		if (process.returncode == 1):
			self.__future.set_result(True)
			return

		from .state import State
		class __Pass(State):
			def __init__(self, next_state: State):
				self.__next_state = next_state
			def handle(self, request: Request) -> State:
				return self.__next_state
			def response(self) -> Response:
				pass

		self.state = __Pass(
			self.state.handle(
				Request(None, process.stdout.strip())
			)
		)
		self.__loop.create_task(self.__run_client())

	def _handle(self, request: Request):
		self.state = self.state.handle(request)

		return self.state \
			and self.state.response() \
			or Response([])

	async def __run_client(self):
		self.__log('__run_client')

		from pathlib import PosixPath
		cmd = PosixPath(sys.argv[0]).resolve().as_posix()
		client = cmd + ' ' + ARG_CLIENT

		self.__process, _protocol = await self.__loop \
			.subprocess_exec(
				self.__client_process,
				'rofi',
				'-modi',
				'client:' + client,
				'-show',
				'client',
				*keybinds.list
			)

		self.__log('client runed')

	def __client_process(self):
		return ClientProcess(self.__client_stopped)

	def __client_stopped(self):
		self.__log('__client_stopped')

		self.stop()
		self.__future.set_result(True)

	async def _read(self):
		return await self.__connection.read()

	def _write(self, data):
		return self.__connection.write(data)

	def _exception_handler(self, loop, context):
		import sys
		sys.excepthook(None, context['exception'], None)

		self.__log('_exception_handler')
		self.stop()

	def stop(self, signal_num = 2, frame = None):
		if (self.__connection):
			self.__connection.close()
			self.__connection = None
			self.__log('connection.close')

		if (self.__process):
			self.__process.get_returncode() is None \
				and self.__process.terminate()

			self.__process.close()
			self.__process = None

		self.__log('stop')

	def __log(self, text):
		logger.debug('[server]: ' + str(text))

	def __del__(self):
		self.stop()
