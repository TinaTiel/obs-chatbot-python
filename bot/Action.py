from bot.Result import *

class Action():

	def __init__(self, restrictions=[], config={}):
		self.restrictions = []
		self.add_restrictions(restrictions if isinstance(restrictions, list) else [])
		self.config = config

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

	def _execute(self, user, args):
		pass