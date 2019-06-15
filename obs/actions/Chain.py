import obswebsocket, obswebsocket.requests
import logging
import time
from obs.actions.Action import Action
from importlib import import_module
from obs.Permission import Permission

class Chain(Action):

	def __init__(self, obs_client, command_name, aliases, description, permission, min_votes, args):
		"""Initializes this class, see Action.py
		"""
		super().__init__(obs_client, command_name, aliases, description, permission, min_votes, args)
		self.log = logging.getLogger(__name__)
		self._init_args(args)

	def execute(self, user):
		"""Shows a scene item, such as an image or video, and then hides it after
		a specified duration
		"""

		# Check user permissions and votes
		if(not (
			self._has_permission(user) 
			and self._has_enough_votes(user) 
			)
		):
			return self._twitch_failed()
		
		# finally execute the commands in the list, in order.
		# Fail the entire chain if one link fails.
		for command_obj in self.command_objs:
			if(not command_obj.execute(user)):
				self._twitch_failed()
				return False

		self._twitch_done()
		return True

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		commands (list): list of commands to execute
		"""

		# Validate the basic piece is in place
		self.commands = args.get('commands', None)
		if(self.commands is None):
			raise ValueError("Command {}: Args error, missing 'commands'".format(self.command_name))

		# Since each command is essentially its own set of commands, validate the 
		# command type and its arguments for each command in the chain
		self.command_objs = []
		for index, command in enumerate(self.commands):
			self.log.debug("Index {}, command {}".format(index, command))
			action = command.get('action', None)
			action_args = command.get('args', None)

			if(action is None or action_args is None):
				raise ValueError("Command Chain {}[{}]: Config error, missing 'action' or 'args'".format(self.command_name, index))

			try:
				module = import_module("obs.actions."+action)
				class_ = getattr(module, action)
				self.log.debug("Command Chain {}[{}]: action is {}".format(self.command_name, index, class_))
			except Exception as e:
				raise ValueError("Command Chain {}[{}]: Error, no such action {} is defined. Full error: {}".format(self.command_name, index, action, e))

			# Try to instantiate the action class
			try:
				self.log.debug("Command Chain {}[{}]: args are: {}".format(self.command_name, index, action_args))
				command_obj = class_(
					self.obs_client, 
					"Chain {}[{}]".format(self.command_name, index), 
					self.aliases, 
					self.description, 
					Permission.EVERYONE, # Effectively ensures this command will execute if permission is granted to parent 
					0, # Effectively ensures this command will execute per parent voting strategy
					action_args)
			except ValueError as e:
				raise e

			# Add command_obj to internal reference
			self.command_objs.append(command_obj)