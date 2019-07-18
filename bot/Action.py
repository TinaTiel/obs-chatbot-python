from bot.Result import *

class Action():

	def __init__(self, **kwargs):
		# restrictions=[], config={}
		restrictions = kwargs.get('restrictions', [])
		args = kwargs.get('args', None)
		if(args is None):
			raise ValueError("Action is missing 'args' configuration")

		self.restrictions = []
		self.add_restrictions(restrictions if isinstance(restrictions, list) else [])
		self._init_args(args)

	def execute(self, user, args):
		if(not self._permit(user)):
			return Result(State.FAILURE, ["Failed restrictions"])
		self._execute(user, args)
		return Result(State.SUCCESS)

	def add_restrictions(self, restrictions):
		for restriction in restrictions:
			self.restrictions.append(restriction)
			restriction.action = self

	def _permit(self, user):
		for restriction in self.restrictions:
			if not restriction.permit(user):
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