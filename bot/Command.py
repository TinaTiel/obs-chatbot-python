import shlex
from bot.Result import *
from bot.Executor import *

class Command():

	def __init__(self, name, description="", aliases=[], actions=[], restrictions=[], executor=ExecutorDefault()):
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
		
		# Build restrictions and actions
		# restrictions = self._build_restrictions(restrictions_confs)
		pass


	def execute(self, command_name, user, args):
		'''
		Executes a particular command
		'''
		pass

	def build_command(self, command_conf):
		# name = config.get('name', None)
		# action_confs = config.get('actions', None)
		# restriction_confs = config.get('restrictions', None)
		# if(name is None or action_confs is None or restriction_confs is None):
		# 	raise ValueError("Command is missing name, actions, or restrictions.")
		# # Get optional args
		# description = config.get('description', "")
		# aliases = config.get('aliases', [])

		# restrictions = [self._build_restriction for conf in restriction_confs]
		# actions = [self._build_action for conf in action_confs]

		# return Command(name, description, aliases, actions, restrictions)
		pass

	def build_restriction(self, restriction_conf):
		# # Get the required config
		# restr_type = conf.get('type', None)
		# restr_args = conf.get('args', None)
		# if(restr_type is None or restr_args is None):
		# 	raise ValueError("Missing type or args")
		
		# # Locate the Restriction type class
		# try:
		# 	module = import_module("bot.Restriction."+restr_type)
		# 	class_ = getattr(module, restr_type)
		# except Exception as e:
		# 	raise ValueError("Could not locate Restriction type '{}'".format(restr_type))

		# # Instantiate the Restriction class
		# try:
		# 	restriction = class_(restr_args**) # Maybe??
		# except ValueError as e:
		# 	raise e
		pass

	def build_action(self, action_conf):
		pass