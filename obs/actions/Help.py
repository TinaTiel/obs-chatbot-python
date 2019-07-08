import obswebsocket, obswebsocket.requests
import logging
import time
from obs.actions.Action import Action
from obs.Permission import Permission
from itertools import groupby

class Help(Action):

	def __init__(self, obs_client, command_name, aliases, description, permission, min_votes, args):
		"""Initializes this class, see Action.py
		"""
		super().__init__(obs_client, command_name, aliases, description, permission, min_votes, args)
		self.log = logging.getLogger(__name__)
		self._init_args(args)

	def execute(self, user):
		"""Shows all the commands available
		"""

		# Get the unique commands from the obs client, excluding this command
		unique_commands = set()
		for key, value in self.obs_client.commands.items():
			# skip the help command, no need to show it if the user called it...
			if(value.command_name == self.command_name):
				continue
			# build tuples, joining aliases into a single string if present
			if(value.aliases is not None and len(value.aliases) > 0):
				aliases = ', '.join(["!" + alias for alias in value.aliases])
			else:
				aliases = None

			unique_commands.add((value.permission, value.command_name, value.description, aliases)) # tuples are hashable, but not dicts ;-)

		

		# Say a shortened version without descriptions, just grouped by permission
		if(self.short is not None and self.short == True):
			unique_commands = sorted(unique_commands, key=lambda x: x[0])
			grouped_commands = {}
			for key, group in groupby(unique_commands, lambda x: x[0]):
				grouped_commands[key.name] = list(group)

			help_str = ""
			for key, value in grouped_commands.items():
				value = sorted(value, key=lambda x: x[1])
				help_str += "{}: {}; ".format(key, ", ".join(["!{}".format(command[1]) for command in value]))
			self._twitch_say(help_str)

		else:
			help_strs = []
			for command in unique_commands:
				help_str = ""
				help_str += "[{}] {}: {}".format(command[0].name, "!" + command[1], command[2])
				if(command[2] is not None):
					help_str += " [aliases: {}]".format(command[3])
				help_strs.append(help_str)
			self._twitch_say(help_strs)

		self._twitch_failed() # force reset the queue so other commands can execute
		return True

	def _init_args(self, args):
		"""Nothing to do"""
		self.short = args.get('short', None) # Optional

	def _get_permission(self, command):
		return command.permission