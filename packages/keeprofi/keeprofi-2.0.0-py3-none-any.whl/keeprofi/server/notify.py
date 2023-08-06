
import asyncio
import desktop_notify.aio as aio

from keeprofi import APP_NAME

server = aio.Server(APP_NAME)

class Notify(aio.Notify):

	def __init__(self, *args):
		super().__init__(*args)
		self.set_server(server)
		self.__loop = asyncio.get_event_loop()

	def show(self):
		runner = self.__loop.is_running() \
			and self.__loop.create_task \
			or self.__loop.run_until_complete

		runner(super().show())
