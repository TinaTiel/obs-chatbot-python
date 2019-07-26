import bot.Common as Common
from bot.Command import *

class CommandClientBase:

	def __init__(self):
		self.commands = {}
		self.disabled = {}

	def load_commands(self, confs):
		'''
		Tries to load each command specified in the confs dict
		'''
		commands = confs.get('commands', None)
		if (commands is None or not isinstance(commands, list)):
			raise ValueError("Missing 'commands' when initializing list of commands, or 'commands' isn't a list")

		for command in commands:
			self.load_command(command)

	def load_command(self, conf):
		'''
		Loads a command specified in the conf dict
		'''
		command = self._build_command(conf)
		self.commands[command.name] = command
		for alias in command.aliases:
			self.commands[alias] = command

	def execute(self, command_name, user, args):
		command = self.commands.get(command_name, None)
		if(command is None):
			return Result(State.FAILURE, "{} is not a command".format(command_name))

		result = command.execute(user, args)
		return Result(State.SUCCESS, result)

	def disable(self, command_name):
		command = self.commands.pop(command_name, None)
		if(command is None):
			return Result(State.FAILURE, "{} is not a command".format(command_name))

		self.disabled[command_name] = command


	def enable(self, command_name):
		pass

	def _build_command(self, conf):
		# Check for required args
		name = conf.get('name', None)
		allows = conf.get('allows', None)
		action = conf.get('action', None)
		if(name is None or allows is None or action is None):
			raise ValueError("Command requires 'name', 'allows', or 'action'")
		
		# Get optional args
		description = conf.get('description', "")
		aliases = conf.get('aliases', [])

		return Command(name, allows, action, description, aliases)

class DummyCommandClient(CommandClientBase):

	def __init__(self):
		pass

	def load_commands(self, confs):
		pass

	def load_command(self, conf):
		pass

	def execute(self, command_name, user, args):
		pass

	def disable(self, command_name):
		pass

	def enable(self, command_name):
		pass

