import obswebsocket, obswebsocket.requests
import logging
import time
from Message import Message

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
		self.min_votes = votes
		self.votes = []
		self._init_args(args)

	def execute(self, user):
		"""Shows a scene item, such as an image or video, and then hides it after
		a specified duration
		"""

		# first check user has permission for this command
		has_permission = Common.eval_permission(user, self.permission)
		if(not has_permission):
			return # TODO: replace with callback on parent

		# then add user to votes and evaluate votes permission
		votes.add(user.name)
		if(not len(votes) >= min_votes):
			return # TODO: replace with callback on parent
		
		# finally execute the command

		# Validate if the user is allowed to execute this command
		if(self._canExecute(user, permission) == False):
			self.log.debug("User {} is NOT permitted to execute {}".format(user['name'], command_name))
			return # TODO: replace with callback on parent
		else:
			self.log.debug("User {} is permitted to execute {}".format(user['name'], command_name))

		# Validate args
		scene_item = args.get('item', None)
		duration = args.get('duration-seconds', None)
		if(scene_item is None or duration is None):
			self.log.warn("Config error: Missing 'item' or 'duration' for showSceneItem command")
			return # TODO: replace with callback on parent

		if(duration <= 0):
			self.log.warn("Config error: Duration cannot be zero or negative!")
			return # TODO: replace with callback on parent

		# Get optional args
		scene = args.get('scene', None)

		res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(scene_item, True, scene))
		if(res.status == False):
			self.log.warn("Could not show scene item {}! Error: {}".format(scene_item, res.datain['error']))
			return # TODO: replace with callback on parent

		time.sleep(duration)
		res = self.obs_client.client.call(obswebsocket.requests.SetSceneItemRender(scene_item, False, scene))
		if(res.status == False):
			self.log.warn("Could not hide scene item {}! Error: {}".format(scene_item, res.datain['error']))
			return # TODO: replace with callback on parent

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		args must contain:
		command_name (string): Name of the command this alias should execute.

		"""
		self.scene_item = args.get('scene_item')
		self.duration = args.get('duration')
		if(self.scene_item is None or self.duration is None):
			raise ValueError("Command {}: Args error, missing 'scene_item' or 'duration' for command".format(self.command_name))

		if(self.duration < 0):
			raise ValueError("Command {}: Args error, duration must be greater than zero".format(self.command_name))