
import pickle

class Connection():

	@classmethod
	async def create(cls, *args):
		return cls(*args)

	def __init__(self, loop, reader, writer, log):
		self.__log = log

		self.__loop = loop

		self.__reader = reader
		self.__writer = writer

	async def read(self):
		message = await self._read_bytes()

		return self._deserialize(message)

	def write(self, data):
		message = self._serialize(data)

		self._write_bytes(message)

	def _serialize(self, data):
		return pickle.dumps(data)

	def _deserialize(self, message):
		return pickle.loads(message)

	async def _read_bytes(self):
		length = await self.__reader.readline()
		if (length):
			self.__log('reading: ' + str(length))
			return await self.__reader.read(
				int(length.decode())
			)

	def _write_bytes(self, message):
		length = (str(len(message)) + '\n').encode()

		self.__log('writing: ' + str(length) + str(message))

		self.__writer.write(length)
		self.__writer.write(message)

	def close(self):
		self.__writer.close()

		self.__loop.create_task(self.__writer.wait_closed())
