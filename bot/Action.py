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
		self.args = args
		self._init_args()

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

	def _init_args(self):
		pass

	def _execute(self, user, args):
		pass