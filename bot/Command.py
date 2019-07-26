import shlex
from bot.Result import *
import bot.Common as Common

class CommandBase():

	def __init__(self, name, allow_confs, executor_conf, description="", aliases=[]):
		self.name = name
		self._build_allows(allow_confs)
		self._build_executor(executor_conf)
		self.description = description
		self.aliases = aliases

	def execute(self, user, args):
		# If not permitted, fail immediately

		if(not self._permit(user)):
			return Result(State.FAILURE, ["Failed Allows/Permissions"])

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

	def _build_executor(self, conf):
		# validate conf isn't a list
		if(isinstance(conf, list)):
			raise ValueError("Root executor configuration cannot be a list. Use an Executor containing Executors instead.")

		# get requiried items
		exec_type = conf.get('type', None)
		args = conf.get('args', None)
		if(exec_type is None or args is None):
			raise ValueError("Command 'execute' configuration is missing 'type' or 'args' configurations.")

		# Try to load the specified class and instantiate it
		try:
			class_ = Common.get_class("Executor", exec_type)
		except Exception:
			try:
				class_ = Common.get_class("Action", exec_type)
			except Exception as e:
				raise ValueError("Specified action/executor '{}' does not exist. Error: {}".format(exec_type, e))
		self.executor = class_(**conf)

	def _build_allows(self, confs):
		# do a type conversion if not a list
		if(not isinstance(confs, list)):
			confs = [confs]
		
		# Build each Allow object from confs
		self.allows = []
		for conf in confs:
			# Get required items
			allow_type = conf.get('type', None)
			args = conf.get('args', None)
			if(allow_type is None or args is None):
				raise ValueError("Command 'allows' configuration is missing 'type' or 'args' configurations.")

			# Try to load specified type & instantiate it
			class_ = Common.get_class("Allow", allow_type)
			self.allows.append(class_(**args))


class DummyCommand(CommandBase):
	def __init__(self, name, allow_confs, executor_conf, description="", aliases=[]):
		self.name = name
		self.aliases = aliases

	def execute(self, user, args):
		pass


class Command(CommandBase):
	def __init__(self, name, allow_confs, executor_conf, description="", aliases=[]):
		super().__init__(name, allow_confs, executor_conf, description, aliases)