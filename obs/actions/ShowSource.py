import obswebsocket, obswebsocket.requests
import logging
import time
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
		res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(self.source, True, self.scene))
		if(res.status == False):
			self.log.warn("Could not show scene item {}! Error: {}".format(self.source, res.datain['error']))
			self._twitch_failed()
			return False

		# wait the specified duration
		time.sleep(self.duration)

		# hide the scene again
		res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(self.source, False, self.scene))
		if(res.status == False):
			self.log.warn("Could not hide scene item {}! Error: {}".format(self.source, res.datain['error']))
			self._twitch_failed()
			return False

		self._twitch_done()
		return True

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		scene item (string): Name of the scene to show.
		duration (int): Duration (seconds) to show scene.

		Optional args:
		scene (string): Name of scene where scene item is nested. If not provided, 
									  then the current scene is used. 
		"""
		self.source = args.get('source', None)
		self.duration = args.get('duration', None)
		self.scene = args.get('scene', None) # This is an optional command
		if(self.source is None or self.duration is None):
			raise ValueError("Command {}: Args error, missing 'source' or 'duration' for command".format(self.command_name))

		if(self.duration < 0):
			raise ValueError("Command {}: Args error, duration must be greater than zero".format(self.command_name))