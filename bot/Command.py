import shlex
from bot.Result import *
from bot.Executor import *

class Command():

	def __init__(self, name, executor, allows=[], description="", aliases=[]):
		self.name = name
		self.executor = executor
		self.allows = allows
		self.description = description
		self.aliases = aliases

	def execute(self, user, args):
		# If not permitted, fail immediately

		if(not self._permit(user)):
			return Result(State.FAILURE, ["Failed allows"])

		# Parse the args
		results = []
		args_list = []
		if(args is not None):
			args_list = shlex.split(args)

		# Execute with user and args
		return self.executor.execute(user, args_list)

	def _permit(self, user):
		# if no allows, never permit
		if(len(self.allows) == 0):
			return False
		# otherwise only succeed if all allows permit
		for allow in self.allows:
			if not allow.permit(user):
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
		
		# Build allows and actions
		# allows = self._build_allows(allows_confs)
		pass


	def execute(self, command_name, user, args):
		'''
		Executes a particular command
		'''
		pass

	def build_command(self, command_conf):
		# Get required confs
		name = config.get('name', None)
		action_confs = config.get('allow', None)
		allow_confs = config.get('allows', None)
		if(name is None or action_confs is None or allow_confs is None):
			raise ValueError("Command is missing name, actions, or allows.")
		# Get optional confs
		description = config.get('description', "")
		aliases = config.get('aliases', [])

		allows = [self._build_allow for conf in allow_confs]
		actions = [self._build_action for conf in action_confs]

		return Command(name, description, aliases, actions, allows)
		pass

	def build_allow(self, allow_conf):
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
		# 	allow = class_(restr_args**) # Maybe??
		# except ValueError as e:
		# 	raise e
		pass

	def build_action(self, action_conf):
		pass