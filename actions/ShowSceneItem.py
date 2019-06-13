import obswebsocket, obswebsocket.requests
import logging
import time
import Common

class ShowSceneItem:

	def __init__(self, obs_client, command_name, permission, min_votes, args):
		"""Initializes this class
		
		Parameters:
		obs_client (ObsClient): Reference to parent object
		command_name (string): chat command associated with this class instance
		permission (Permission): Permission level associated with command TODO: Use this??
		args (object): Arguments for this class instance, such as scene name, duration, etc.

		"""
		self.log = logging.getLogger(__name__)
		self.obs_client = obs_client
		self.command_name = command_name
		self.permission = permission
		self.min_votes = min_votes
		self.votes = set()
		self._init_args(args)

	def execute(self, user):
		"""Shows a scene item, such as an image or video, and then hides it after
		a specified duration
		"""

		# first check user has permission for this command
		has_permission = Common.eval_permission(user, self.permission)
		if(not has_permission):
			self.log.debug("Command {}: User has insufficient privileges".format(self.command_name, user['name']))
			return # TODO: replace with callback on parent

		# then add user to votes and evaluate votes permission
		self.votes.add(user['name'])
		if(not len(self.votes) >= self.min_votes):
			self.log.debug("Command {}: Insufficient votes, {} received of {} required.".format(self.command_name, len(self.votes), self.min_votes))
			return # TODO: replace with callback on parent
		self.votes = set()
		
		# finally execute the command
		# show the scene
		res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(self.scene_item, True, self.scene))
		if(res.status == False):
			self.log.warn("Could not show scene item {}! Error: {}".format(self.scene_item, res.datain['error']))
			return # TODO: replace with callback on parent

		# wait the specified duration
		time.sleep(self.duration)

		# hide the scene again
		res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(self.scene_item, False, self.scene))
		if(res.status == False):
			self.log.warn("Could not hide scene item {}! Error: {}".format(self.scene_item, res.datain['error']))
			return # TODO: replace with callback on parent

		return # TODO: replace with callback on parent

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
		self.scene_item = args.get('scene_item')
		self.duration = args.get('duration')
		self.scene = args.get('scene', None) # This is an optional command
		if(self.scene_item is None or self.duration is None):
			raise ValueError("Command {}: Args error, missing 'scene_item' or 'duration' for command".format(self.command_name))

		if(self.duration < 0):
			raise ValueError("Command {}: Args error, duration must be greater than zero".format(self.command_name))