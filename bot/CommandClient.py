class CommandClientBase:

	def __init__(self):
		self.commands = []

	def load_commands(self, confs):
		commands = confs.get('commands', None)
		if (commands is None or not isinstance(commands, list)):
			raise ValueError("Missing 'commands' when initializing list of commands, or 'commands' isn't a list")

		for command in commands:
			self.load_command(command)

	def load_command(self, conf):
		pass

class DummyCommandClient(CommandClientBase):

	def __init__(self):
		pass

	def load_commands(self, confs):
		pass

	def load_command(self, conf):
		pass