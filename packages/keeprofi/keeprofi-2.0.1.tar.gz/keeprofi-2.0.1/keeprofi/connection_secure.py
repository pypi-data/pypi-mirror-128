
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import (
	serialization,
	hashes,
)
from cryptography.hazmat.primitives.asymmetric.x448 import (
	X448PrivateKey,
	X448PublicKey,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from . import Connection

class ConnectionSecure(Connection):

	KEY_SIZE = 32

	@classmethod
	async def create(cls, *args):
		instance = await super(cls, cls).create(*args)

		return await instance.handshake()

	async def handshake(self):
		private_key = X448PrivateKey.generate()
		self._write_bytes(
			private_key.public_key().public_bytes(
				encoding = serialization.Encoding.Raw,
				format = serialization.PublicFormat.Raw,
			)
		)
		public_bytes = await self._read_bytes()
		public_key = X448PublicKey.from_public_bytes(public_bytes)

		shared_key = private_key.exchange(public_key)

		derived_key = HKDF(
			algorithm = hashes.SHA256(),
			length = self.KEY_SIZE,
			salt = None,
			info = None,
		)\
			.derive(shared_key)

		self.__fernet = Fernet(base64.b64encode(derived_key))

		return self

	def _serialize(self, data):
		message = super()._serialize(data)

		return self.__fernet.encrypt(message)

	def _deserialize(self, ciphertext):
		message = self.__fernet.decrypt(ciphertext)

		return super()._deserialize(message)
