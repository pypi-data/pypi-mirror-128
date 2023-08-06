
import asyncio

APP_NAME = __name__
__SOCKET_ADDRESS = '/tmp/' + APP_NAME + '.sock'
__SOCKET_FAMILY = 'AF_UNIX'
__ARG_CLIENT = '--client'

from .logger import logger
from .connection import Connection
from .connection_secure import ConnectionSecure
from .request import Request
from .response import Response

def main():
	def client(args):
		from .client import Client

		client = Client()
		asyncio.run(client.connect(args))

	def server(args):
		from .server import Server

		server = Server()
		asyncio.run(server.start())

	import argparse

	parser = argparse.ArgumentParser(
		prog = APP_NAME,
		description = 'Fast rofi drun menu for keepass database',
	)
	parser.add_argument(
		__ARG_CLIENT,
		dest = 'client',
		# action = 'store_true',
		nargs='*',
		default = False,
		required = False,
		help = argparse.SUPPRESS,
	)

	args = parser.parse_args()

	(server, client)[
		type(args.client) is list
	](args.client)

