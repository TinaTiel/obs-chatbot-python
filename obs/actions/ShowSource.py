import obswebsocket, obswebsocket.requests
import logging
import time
import random
from obs.actions.Action import Action

class ShowSource(Action):

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
		
		# finally execute the command
		# show the scene
		choice = random.choice(self.source)

		res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(choice, True, self.scene))
		if(res.status == False):
			self.log.warn("Could not show scene item {}! Error: {}".format(choice, res.datain['error']))
			self._twitch_failed()
			return False

		# if a duration was specified then sleep and then hide the scene
		if(self.duration is not None):
			# wait the specified duration
			time.sleep(self.duration)

			# hide the scene again
			res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(choice, False, self.scene))
			if(res.status == False):
				self.log.warn("Could not hide scene item {}! Error: {}".format(choice, res.datain['error']))
				self._twitch_failed()
				return False

		self._twitch_done()
		return True

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		scene item (string): Name of the scene to show.
		
		Optional args:
		scene (string): Name of scene where scene item is nested. If not provided, 
									  then the current scene is used. 
		duration (int): Duration (seconds) to show scene.
		"""
		self.source = args.get('source', None)
		self.duration = args.get('duration', None) # Optional
		self.scene = args.get('scene', None) # Optional

		if(self.source is None or len(self.source) == 0):
			raise ValueError("Command {}: Args error, missing 'source' for command or is empty list".format(self.command_name))

		if(self.duration is not None and self.duration < 0):
			raise ValueError("Command {}: Args error, duration must be greater than zero".format(self.command_name))