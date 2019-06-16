import obswebsocket, obswebsocket.requests
import logging
import time
from obs.actions.Action import Action
from obs.Permission import Permission

class Wait(Action):

	def __init__(self, obs_client, command_name, aliases, description, permission, min_votes, args):
		"""Initializes this class, see Action.py
		"""
		super().__init__(obs_client, command_name, aliases, description, permission, min_votes, args)
		self.log = logging.getLogger(__name__)
		self._init_args(args)

	def execute(self, user):
		"""Waits a specified duration
		"""
		# Check user permissions and votes
		if(not (
			self._has_permission(user) 
			and self._has_enough_votes(user) 
			)
		):
			self._twitch_failed()
			return False
		
		# finally wait the specified duration in seconds
		time.sleep(self.duration)
		self._twitch_failed()

		return True

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		duration (integer): Seconds to wait
		"""

		# Validate the basic piece is in place
		self.duration = args.get('duration', None)

		if(self.duration is None or self.duration < 0):
			raise ValueError("Command {}: Args error, duration must be greater than zero".format(self.command_name))