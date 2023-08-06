
class Request():

	def __init__(self, action, selection):
		self.__action = action
		self.__selection = selection

	@property
	def action(self):
		return self.__action

	@property
	def selection(self):
		return self.__selection
