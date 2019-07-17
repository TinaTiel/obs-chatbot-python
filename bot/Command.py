import shlex
from bot.Result import *
from bot.Executor import *

class Command():

	def __init__(self, name, executor, restrictions=[], description="", aliases=[]):
		self.name = name
		self.executor = executor
		self.restrictions = restrictions
		self.description = description
		self.aliases = aliases

	def execute(self, user, args):
		# If not permitted, fail immediately

		if(not self._permit(user)):
			return Result(State.FAILURE, ["Failed restrictions"])

		# Parse the args
		results = []
		args_list = []
		if(args is not None):
			args_list = shlex.split(args)

		# Execute with user and args
		return self.executor.execute(user, args_list)

	def _permit(self, user):
		# if no restrictions, never permit
		if(len(self.restrictions) == 0):
			return False
		# otherwise only succeed if all restrictions permit
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
		
		# # Locate the Allow type class
		# try:
		# 	module = import_module("bot.Allow."+restr_type)
		# 	class_ = getattr(module, restr_type)
		# except Exception as e:
		# 	raise ValueError("Could not locate Allow type '{}'".format(restr_type))

		# # Instantiate the Allow class
		# try:
		# 	restriction = class_(restr_args**) # Maybe??
		# except ValueError as e:
		# 	raise e
		pass

	def build_action(self, action_conf):
		pass