import obswebsocket, obswebsocket.requests
import logging
import time
from obs.actions.Action import Action
from obs.Permission import Permission

class Say(Action):

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
			self._twitch_failed()
			return False
		
		# finally say the messages in order, no cooldown
		for message in self.messages:
			self.log.debug("Saying: " + message)
			self._twitch_say(message)
			self._twitch_failed()
		
		return True

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		commands (list): list of commands to execute
		"""

		# Validate the basic piece is in place
		self.messages = args.get('messages', None)
		if(self.messages is None):
			raise ValueError("Command {}: Args error, missing 'messages'".format(self.command_name))