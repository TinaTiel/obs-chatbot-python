import obswebsocket, obswebsocket.requests
import logging
import time
from obs.actions.Action import Action

class ShowScene(Action):
	def __init__(self, obs_client, command_name, aliases, description, permission, min_votes, args):
		"""Initializes this class, see Action.py
		"""
		super().__init__(obs_client, command_name, aliases, description, permission, min_votes, args)
		self.log = logging.getLogger(__name__)
		self._init_args(args)

	def execute(self, user):
		"""Permanently switches to a specified scene
		"""
		# Check user permissions and votes
		if(not (
			self._has_permission(user) 
			and self._has_enough_votes(user) 
			)
		):
			self._twitch_failed()
			return False
		
		# finally execute the command
		# if a duration was provided, then switch back to the originating scene after duration
		# otherwise just permanently switch to the scene
		if(self.duration is not None):
			starting_scene = self.obs_client.client.call(obswebsocket.requests.GetCurrentScene()).getName()

			# switch to the desired scene
			res = self.obs_client.client.call(obswebsocket.requests.SetCurrentScene(self.scene))
			if(res.status == False):
				self.log.warn("Could not set scene! Error: {}".format(res.datain['error']))
				self._twitch_failed()
				return False

			# wait the specified duration
			time.sleep(self.duration)

			# switch back to the starting scene
			res = self.obs_client.client.call(obswebsocket.requests.SetCurrentScene(starting_scene))
			if(res.status == False):
				self.log.warn("Could not set scene! Error: {}".format(res.datain['error']))
				self._twitch_failed()
				return False

		else:
			res = self.obs_client.client.call(obswebsocket.requests.SetCurrentScene(self.scene))
			if(res.status == False):
				self.log.warn("Could not set scene! Error: {}".format(res.datain['error']))
				self._twitch_failed()
				return False

		self._twitch_done()
		return True

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		scene (string): Name of the scene to switch to

		Optional args:
		duration (integer): Time to show scene before returning to starting scene.
		"""
		self.scene = args.get('scene', None) 
		self.duration = args.get('duration', None) # Optional
		if(self.scene is None):
			raise ValueError("Command {}: Args error, missing 'scene' for command".format(self.command_name))

		if(self.duration is not None and self.duration < 0):
			raise ValueError("Command {}: Args error, duration must be greater than zero".format(self.command_name))
