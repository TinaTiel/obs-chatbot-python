import obswebsocket, obswebsocket.requests
import logging
import time
from obs.actions.Action import Action

class SetScene(Action):
	def __init__(self, obs_client, command_name, description, permission, min_votes, args):
		"""Initializes this class
		
		Parameters:
		obs_client (ObsClient): Reference to parent object
		command_name (string): chat command associated with this class instance
		permission (Permission): Permission level associated with command TODO: Use this??
		args (object): Arguments for this class instance, such as scene name, duration, etc.

		"""
		super().__init__(obs_client, command_name, description, permission, min_votes, args)
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
			return
		
		# finally execute the command
		res = self.obs_client.client.call(obswebsocket.requests.SetCurrentScene(self.scene))
		if(res.status == False):
			self.log.warn("Could not set scene! Error: {}".format(res.datain['error']))

	def _init_args(self, args):
		"""This validates the arguments are valid for this instance, 
		and raises a ValueError if they aren't.

		Mandatory args:
		scene (string): Name of the scene to switch to
		"""
		self.scene = args.get('scene', None) 
		if(self.scene is None):
			raise ValueError("Command {}: Args error, missing 'scene' for command".format(self.command_name))
