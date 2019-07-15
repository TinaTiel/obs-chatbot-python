from enum import Enum
import shlex

class Command():

	def __init__(self, name, description, aliases=[], actions=[], restrictions=[]):
		self.name = name
		self.description = description
		self.aliases = aliases if isinstance(aliases, list) else []
		self.actions = actions if isinstance(actions, list) else []
		self.restrictions = restrictions if isinstance(restrictions, list) else []

	def execute(self, user, args):
		# If not permitted, fail immediately

		if(not self._permit(user)):
			return Result(State.FAILURE, ["Failed restrictions"])

		# Parse the args
		results = []
		args_list = []
		if(args is not None):
			args_list = shlex.split(args)

		# Execute each action with user and args
		for action in self.actions:
			result = action.execute(user, args_list)
			results.append(result)

			# If an action failed, exit early
			if(result.state == State.FAILURE):
				return Result(State.FAILURE, results)

		# Return success
		return Result(State.SUCCESS, results)

	def _permit(self, user):
		for restriction in self.restrictions:
			if not restriction.permit(user):
				return False
		return True


class Action():

	def __init__(self):
		pass

	def execute(self, user, args):
		pass


class Restriction():
	def __init__(self):
		pass

	def permit(self, user):
		pass

class Result():
	def __init__(self, state, messages=[]):
		self.state = state
		self.messages = messages


class State(Enum):
	FAILURE = 1
	SUCCESS = 2
	WORKING = 3