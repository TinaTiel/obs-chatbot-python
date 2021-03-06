import obswebsocket, obswebsocket.requests
import logging
import time
from obs.actions.Action import Action
from obs.Permission import Permission
import random

class Say(Action):

	def __init__(self, obs_client, command_name, aliases, description, permission, min_votes, args):
		"""Initializes this class, see Action.py
		"""
		super().__init__(obs_client, command_name, aliases, description, permission, min_votes, args)
		self.log = logging.getLogger(__name__)
		self._init_args(args)

	def execute(self, user):
		"""Says specified text in chat
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
		if self.random == True:
			if(len(self.messages) == 0):
				self.messages = self.picked_items
				self.picked_items = []

			choice = self.messages.pop(random.randrange(len(self.messages)))
			self.picked_items.append(choice)
			self._twitch_say(choice)

		else:
			self._twitch_say(self.messages)

		self._twitch_failed()
		return True

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		messages (list): list of messages to say
		"""

		# Validate the basic piece is in place
		self.messages = args.get('messages', None)
		self.random = args.get('random', False)
		if self.random == True:
			self.picked_items = []

		if(self.messages is None):
			raise ValueError("Command {}: Args error, missing 'messages'".format(self.command_name))