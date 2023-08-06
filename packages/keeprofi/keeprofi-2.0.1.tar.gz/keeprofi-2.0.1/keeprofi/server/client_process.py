
import asyncio

class ClientProcess(asyncio.SubprocessProtocol):

	def __init__(self, exit_handler):
		self.__exit_handler = exit_handler

	def process_exited(self):
		self.__exit_handler()
