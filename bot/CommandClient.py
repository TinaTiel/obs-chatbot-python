class CommandClientBase:

	def __init__(self):
		self.commands = {}

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

	def _build_command(self, conf):
		pass

class DummyCommandClient(CommandClientBase):

	def __init__(self):
		pass

	def load_commands(self, confs):
		pass

	def load_command(self, conf):
		pass