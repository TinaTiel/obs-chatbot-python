from bot.Result import *

class Action():

	def __init__(self, **kwargs):
		allows = kwargs.get('allows', [])
		args = kwargs.get('args', None)
		if(args is None):
			raise ValueError("Action is missing 'args' configuration")

		self.allows = []
		self.add_allows(allows if isinstance(allows, list) else [])
		self._init_args(args)

	def execute(self, user, args):
		if(not self._permit(user)):
			return Result(State.FAILURE, ["Failed allows"])
		self._execute(user, args)
		return Result(State.SUCCESS)

	def add_allows(self, allows):
		for allow in allows:
			self.allows.append(allow)
			allow.action = self

	def _permit(self, user):
		for allow in self.allows:
			if not allow.permit(user):
				return False
		return True

	def _init_args(self, args):
		pass

	def _execute(self, user, args):
		pass

class AnyArgs(Action):
	'''A dummy Action class
	that takes args provided
	'''
	def __init__(self, **kwargs):
		super().__init__(kwargs)

	def _init_args(self, args):
		self.args = args

	def _execute(self, user, args):
		pass