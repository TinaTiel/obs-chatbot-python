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
		commands = self._validate_commands_conf(confs)

		for command in commands:
			self.load_command(command)

	def load_command(self, conf):
		'''
		Loads a command specified in the conf dict
		'''
		command = self._build_command(conf)
		self._add_command_to_container(command, self.commands)

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
		for alias in command.aliases:
			self.disabled[alias] = self.commands.pop(alias)
		return Result(State.SUCCESS)

	def enable(self, command_name):
		command = self.disabled.pop(command_name, None)
		if(command is None):
			return Result(State.FAILURE, "{} is not a command".format(command_name))
		self.commands[command_name] = command
		for alias in command.aliases:
			self.commands[alias] = self.disabled.pop(alias)
		return Result(State.SUCCESS)

	def reload_commands(self, confs):
		command_confs = self._validate_commands_conf(confs)
		tmp = {}
		try:
			for conf in command_confs:
				command = self._build_command(conf)
				self._add_command_to_container(command, tmp)
		except ValueError:
			return Result(State.FAILURE, "Invalid configuration")
		self.commands.clear()
		self.commands.update(tmp)

	def _validate_commands_conf(self, confs):
		command_confs = confs.get('commands', None)
		if (command_confs is None or not isinstance(command_confs, list)):
			raise ValueError("Missing 'commands' when initializing list of commands, or 'commands' isn't a list")
		return command_confs

	def _add_command_to_container(self, command, container):
		container[command.name] = command
		for alias in command.aliases:
			container[alias] = command

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

	def reload_commands(self, confs):
		pass
