import obswebsocket, obswebsocket.requests
import logging
import time
import Common

class SetScene():
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
		"""Permanently switches to a specified scene
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
