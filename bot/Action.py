from bot.Result import *

class ActionBase():

	def __init__(self, parent=None, lvl=0, **kwargs):
		self.parent = parent
		self.lvl = lvl
		allows = kwargs.get('allows', [])
		args = kwargs.get('args', None)
		if(args is None):
			raise ValueError("Action is missing 'args' configuration. Config provided: {}".format(kwargs))

		self.allows = []
		self.add_allows(allows if isinstance(allows, list) else [])
		self.args = args
		self._init_args()

	def __repr__(self):
		return "{}{}={{args: {}}}".format("\t"*(self.lvl), self.__class__.__name__, str(self.args))

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

	def _init_args(self):
		pass

	def _execute(self, user, args):
		pass

class DummyAction(ActionBase):
	'''A dummy Action class
	that takes args provided
	'''
	def __init__(self, parent=None, lvl=0, **kwargs):
		self.allows = []
		self.args = {}

	def _init_args(self):
		pass

	def _execute(self, user, args):
		pass