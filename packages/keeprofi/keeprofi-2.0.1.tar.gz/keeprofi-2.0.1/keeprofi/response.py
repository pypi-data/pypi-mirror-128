
class Response():

	def __init__(self, ls, prompt = None, custom = False):
		self.__ls = ls
		self.__prompt = prompt or 'p: '
		self.__custom = custom

	@property
	def ls(self):
		return self.__ls

	@property
	def prompt(self):
		return self.__prompt

	@property
	def custom(self):
		return self.__custom
