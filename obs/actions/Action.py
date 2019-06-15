import obswebsocket, obswebsocket.requests
import logging
import time
from obs.Common import eval_permission

class Action:

	def __init__(self, obs_client, command_name, description, permission, min_votes, args):
		"""Initializes this class
		
		Parameters:
		obs_client (ObsClient): Reference to parent object
		command_name (string): chat command associated with this class instance
		description (string): description of the chat command
		permission (Permission): Permission level associated with command
		min_votes (string): minimimum votes required for the command to execute
		args (object): Arguments for this class instance, such as scene name, duration, etc.
		"""

		self.log = logging.getLogger(__name__)
		self.obs_client = obs_client
		self.command_name = command_name
		self.permission = permission
		self.min_votes = min_votes
		self.votes = set()

	def execute(self, user):
		raise NotImplementedError("The action isn't defined!")

	def _sufficient_votes(self, user):
		self.votes.add(user['name'])
		if(not len(self.votes) >= self.min_votes):
			self.log.debug("Command {}: Insufficient votes, {} received of {} required.".format(self.command_name, len(self.votes), self.min_votes))
			return False # TODO: replace with callback on parent
		self.votes = set()
		self.log.debug("Command {}: All votes received".format(self.command_name))
		return True