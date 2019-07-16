import shlex
from bot.Result import *

class Command():

	def __init__(self, name, description="", aliases=[], actions=[], restrictions=[]):
		self.name = name
		self.description = description
		self.aliases = aliases if isinstance(aliases, list) else []
		self.actions = []
		self.restrictions = []
		self.add_actions(actions if isinstance(actions, list) else [])
		self.add_restrictions(restrictions if isinstance(restrictions, list) else [])

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

	def add_actions(self, actions):
		for action in actions:
			self.actions.append(action)
			action.command = self

	def add_restrictions(self, restrictions):
		for restriction in restrictions:
			self.restrictions.append(restriction)
			restriction.command = self

	def _permit(self, user):
		for restriction in self.restrictions:
			if not restriction.permit(user):
				return False
		return True

class CommandManager():

	def __init__(self):
		pass

	def register(self, config):
		'''
		builds and registers a command with this manager
		'''
		# Get required args
		name = config.get('name', None)
		actions = config.get('actions', None)
		restrictions = config.get('restrictions', None)
		if(name is None or actions is None or restrictions is None):
			raise ValueError("Command is missing name, actions, or restrictions.")
		# Get optional args
		description = config.get('description', "")
		aliases = config.get('aliases', [])

	def execute(self, command_name, user, args):
		'''
		Executes a particular command
		'''
		pass